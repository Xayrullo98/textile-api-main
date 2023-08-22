from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.clients import Clients
from models.currencies import Currencies
from models.orders import Orders
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_orders(page, limit, db):
    orders = db.query(Orders).options(
        joinedload(Orders.client), joinedload(Orders.currency), joinedload(Orders.user),
        joinedload(Orders.category)
    )

    if page and limit:
        return pagination(orders, page, limit)
    else:
        return orders


def one_order(ident, db):
    the_item = db.query(Orders).options(
        joinedload(Orders.currency), joinedload(Orders.category), joinedload(Orders.user),
        joinedload(Orders.client)).filter(Orders.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order(form, db, thisuser):
    the_one(db, Clients, form.client_id, thisuser)
    the_one(db, Categories, form.category_id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    new_order_db = Orders(
        client_id=form.client_id,
        date=date.now(),
        quantity=form.quantity,
        category_id=form.category_id,
        price=form.price,
        currency_id=form.currency_id,
        delivery_date=form.delivery_date,
        status=form.status,
        order_status=form.order_status,
        user_id=thisuser.id,

    )
    save_in_db(db, new_order_db)


def update_order(form, db, thisuser):
    the_one(db, Orders, form.id, thisuser)
    the_one(db, Clients, form.client_id, thisuser)
    the_one(db, Categories, form.category_id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.client_id: form.client_id,
        Orders.quantity: form.quantity,
        Orders.price: form.price,
        Orders.currency_id: form.currency_id,
        Orders.category_id: form.category_id,
        Orders.delivery_date: form.delivery_date,
        Orders.status: form.status,
        Orders.order_status: form.order_status,
        Orders.user_id: thisuser.id
    })
    db.commit()
