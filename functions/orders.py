from datetime import date, datetime

from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload, subqueryload

from functions.incomes import add_income
from functions.kassa import one_kassa, one_kassa_via_currency_id
from functions.order_histories import create_order_history
from functions.users import add_user_balance
from models.categories import Categories
from models.clients import Clients
from models.currencies import Currencies
from models.orders import Orders
from models.phones import Phones
from models.stage_users import Stage_users
from models.stages import Stages

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_orders(search, client_id, category_id, currency_id, stage_id, from_date, to_date, page, limit, db):
    orders = db.query(Orders).join(Orders.category).options(
        joinedload(Orders.client).options(subqueryload(Clients.client_phones)), joinedload(Orders.currency), joinedload(Orders.user),
        joinedload(Orders.category), joinedload(Orders.stage))

    if search:
        search_formatted = f"%{search}%"
        orders = orders.filter(Categories.name.like(search_formatted))
    if client_id:
        orders = orders.filter(Orders.client_id == client_id)
    if from_date and to_date:
        orders = orders.filter(func.date(Orders.date).between(from_date, to_date))
    if category_id:
        orders = orders.filter(Orders.category_id == category_id)
    if currency_id:
        orders = orders.filter(Orders.currency_id == currency_id)
    if stage_id:
        orders = orders.filter(Orders.stage_id == stage_id)
    orders = orders.order_by(Orders.id.desc())
    return pagination(orders, page, limit)


def one_order(ident, db):
    the_item = db.query(Orders).options(
        joinedload(Orders.currency), joinedload(Orders.category), joinedload(Orders.user),
        joinedload(Orders.client).options(subqueryload(Clients.client_phones))).filter(Orders.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order(form, db, thisuser):
    the_one(db, Clients, form.client_id)
    the_one(db, Categories, form.category_id)
    the_one(db, Currencies, form.currency_id)
    new_order_db = Orders(
            client_id=form.client_id,
            date=datetime.now(),
            quantity=form.quantity,
            category_id=form.category_id,
            price=form.price,
            currency_id=form.currency_id,
            delivery_date=form.delivery_date,
            stage_id=0,
            order_status=False,
            user_id=thisuser.id,
    )
    save_in_db(db, new_order_db)
    kassa = one_kassa_via_currency_id(currency_id=form.currency_id,db=db)
    add_income(currency_id=form.currency_id,money=form.price*form.quantity,
               source='order', source_id=new_order_db.id, kassa_id=kassa.id, db=db, thisuser=thisuser)



    #order history will be added after order, kpi_money should be calculated
    kpi_money = 0

    #agar kiritilayotgan quantitydagi mahsulot
    #omborda bo'lsa, ombordan ayriladi va income bo'ladi
    # warehouse_product = db.query(Warehouse_products).filter(Warehouse_products.category_detail)

def update_order(form, db, thisuser):
    order = the_one(db, Orders, form.id)
    if order.stutus == True:
        raise HTTPException(status_code=400, detail="Bu order allaqachon tugatilgan")
    the_one(db, Clients, form.client_id)
    the_one(db, Categories, form.category_id)
    the_one(db, Currencies, form.currency_id)
    stage = the_one(db, Stages, form.stage_id)
    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.client_id: form.client_id,
        Orders.quantity: form.quantity,
        Orders.price: form.price,
        Orders.date: datetime.now(),
        Orders.currency_id: form.currency_id,
        Orders.category_id: form.category_id,
        Orders.delivery_date: form.delivery_date,
        Orders.stage_id: form.stage_id,
        Orders.order_status: form.order_status,
        Orders.user_id: thisuser.id
    })
    db.commit()
    # shu yerda order history ga qo'shib ketamiz
    create_order_history(order.id, form.stage_id, stage.kpi, thisuser.id, db)
    #connected_user larni balansiga stagedagi kpi money qo'shiladi
    stage_users = db.query(Stage_users).filter(Stage_users.stage_id == stage.id).all()
    for stage_user in stage_users:
        add_user_balance(stage_user.connected_user_id, stage.kpi, db)


def update_order_stage(order_id, stage_id, db):

    db.query(Orders).filter(Orders.id == order_id).update({
        Orders.stage_id: stage_id })
    db.commit()


def order_delete(id, db):
    order = the_one(db, Orders, id)
    if order.stage_id != 0:
        raise HTTPException(status_code=400, detail="Orderni faqat stage_id=0 ga teng bo'lganda o'chirish mumkin")
    db.query(Orders).filter(Orders.id == id).delete()
    db.commit()

