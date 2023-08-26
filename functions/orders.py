from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from functions.order_histories import create_order_history, update_order_history
from models.categories import Categories
from models.clients import Clients
from models.currencies import Currencies
from models.orders import Orders
from models.stages import Stages
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_orders(client_id, category_id, currency_id, stage_id, from_date, to_date, page, limit, db):
    orders = db.query(Orders).options(
        joinedload(Orders.client), joinedload(Orders.currency), joinedload(Orders.user),
        joinedload(Orders.category))
    if client_id:
        orders = orders.filter(Orders.client_id == client_id)
    elif from_date and to_date:
        orders = orders.filter(and_(Orders.date >= from_date, Orders.date <= to_date))
    elif category_id:
        orders = orders.filter(Orders.category_id == category_id)
    elif currency_id:
        orders = orders.filter(Orders.currency_id == currency_id)
    elif stage_id:
        orders = orders.filter(Orders.stage_id == stage_id)

    return pagination(orders, page, limit)


def one_order(ident, db):
    the_item = db.query(Orders).options(
        joinedload(Orders.currency), joinedload(Orders.category), joinedload(Orders.user),
        joinedload(Orders.client)).filter(Orders.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order(form, db, thisuser):
    the_one(db, Clients, form.client_id)
    the_one(db, Categories, form.category_id)
    the_one(db, Currencies, form.currency_id)
    the_one(db, Stages, form.stage_id)
    new_order_db = Orders(
        client_id=form.client_id,
        date=date.today(),
        quantity=form.quantity,
        category_id=form.category_id,
        price=form.price,
        currency_id=form.currency_id,
        delivery_date=form.delivery_date,
        stage_id=form.stage_id,
        order_status=form.order_status,
        user_id=thisuser.id,
    )
    save_in_db(db, new_order_db)
    #order history will be added after order, kpi_money should be calculated
    kpi_money = 0,
    create_order_history(new_order_db.id, form.stage_id, kpi_money, thisuser, db)


def update_order(form, db, thisuser):
    the_one(db, Orders, form.id)
    the_one(db, Clients, form.client_id)
    the_one(db, Categories, form.category_id)
    the_one(db, Currencies, form.currency_id)
    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.client_id: form.client_id,
        Orders.quantity: form.quantity,
        Orders.price: form.price,
        Orders.currency_id: form.currency_id,
        Orders.category_id: form.category_id,
        Orders.delivery_date: form.delivery_date,
        Orders.stage_id: form.stage_id,
        Orders.order_status: form.order_status,
        Orders.user_id: thisuser.id
    })
    db.commit()
    #shu yerda order histiry ni update qilyapmiz
    # id, order_id, stage_id, kpi_money, db, thisuser
    # update_order_history()
def update_order_stage(order_id,stage_id,db):

    db.query(Orders).filter(Orders.id == order_id).update({
        Orders.stage_id: stage_id })
    db.commit()