from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload, subqueryload

from functions.incomes import add_income
from functions.kassa import one_kassa_via_currency_id

from models.categories import Categories
from models.clients import Clients
from models.currencies import Currencies
from models.orders import Orders
from models.stage_users import Stage_users
from models.stages import Stages

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_orders(search, user_id, client_id, category_id, currency_id,  from_date, to_date, page, limit, db):
    orders = db.query(Orders).join(Orders.category).options(
        joinedload(Orders.client).options(subqueryload(Clients.client_phones)), joinedload(Orders.currency),
        joinedload(Orders.user),
        joinedload(Orders.category))
    orders_for_price = db.query(Orders, func.sum(Orders.price * Orders.quantity).label("total_price")).options\
        (joinedload(Orders.currency))

    if search:
        search_formatted = f"%{search}%"
        orders = orders.filter(Categories.name.like(search_formatted))
        orders_for_price = orders_for_price.filter(Categories.name.like(search_formatted))
    if client_id:
        orders = orders.filter(Orders.client_id == client_id)
        orders_for_price = orders_for_price.filter(Orders.client_id == client_id)
    if user_id:
        orders = orders.filter(Orders.user_id == user_id)
        orders_for_price = orders_for_price.filter(Orders.user_id == user_id)
    if from_date and to_date:
        orders = orders.filter(func.date(Orders.date).between(from_date, to_date))
        orders_for_price = orders_for_price.filter(func.date(Orders.date).between(from_date, to_date))
    if category_id:
        orders = orders.filter(Orders.category_id == category_id)
        orders_for_price = orders_for_price.filter(Orders.category_id == category_id)
    if currency_id:
        orders = orders.filter(Orders.currency_id == currency_id)
        orders_for_price = orders_for_price.filter(Orders.currency_id == currency_id)

    orders = orders.order_by(Orders.id.desc())
    price_data = []
    orders_for_price = orders_for_price.group_by(Orders.currency_id).all()
    for order in orders_for_price:
        price_data.append({"total_price": order.total_price, "currency": order.Orders.currency.name})
    return {"data": pagination(orders, page, limit), "price_data": price_data}


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
        production_quantity=form.production_quantity,
        category_id=form.category_id,
        price=form.price,
        currency_id=form.currency_id,
        delivery_date=form.delivery_date,
        order_status=False,
        user_id=thisuser.id,
    )
    save_in_db(db, new_order_db)
    kassa = one_kassa_via_currency_id(currency_id=form.currency_id, db=db)
    add_income(currency_id=form.currency_id, money=form.price * form.quantity,
               source='order', source_id=new_order_db.id, kassa_id=kassa.id, db=db, thisuser=thisuser)

    # order history will be added after order, kpi_money should be calculated
    kpi_money = 0

    # agar kiritilayotgan quantitydagi mahsulot
    # omborda bo'lsa, ombordan ayriladi va income bo'ladi
    # warehouse_product = db.query(Warehouse_products).filter(Warehouse_products.category_detail)


def update_order(form, thisuser, db):
    order = the_one(db, Orders, form.id)
    if order.order_status == True:
        raise HTTPException(status_code=400, detail="Bu order allaqachon tugatilgan")
    the_one(db, Clients, form.client_id)
    the_one(db, Categories, form.category_id)
    the_one(db, Currencies, form.currency_id)


    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.client_id: form.client_id,
        Orders.quantity: form.quantity,
        Orders.production_quantity: form.production_quantity,
        Orders.price: form.price,
        Orders.date: datetime.now(),
        Orders.currency_id: form.currency_id,
        Orders.category_id: form.category_id,
        Orders.delivery_date: form.delivery_date,
        Orders.order_status: form.order_status,
        Orders.user_id: thisuser.id
    })
    db.commit()

    # connected_user larni balansiga stagedagi kpi money qo'shiladi
    # if form.order_status == True:
    #     # shu yerda order history ga qo'shib ketamiz
    #
    #     stage_users = db.query(Stage_users).filter(Stage_users.stage_id == 1).all()
    #     for stage_user in stage_users:
    #         add_user_balance(stage_user.connected_user_id, stage.kpi, db)

#
# def update_order_stage(order_id, stage_id, db):
#     db.query(Orders).filter(Orders.id == order_id).update({
#         Orders.stage_id: stage_id})
#     db.commit()


def order_delete(id, db):
    order = the_one(db, Orders, id)
    db.query(Orders).filter(Orders.id == id).delete()
    db.commit()
