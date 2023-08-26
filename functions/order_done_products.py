from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from functions.order_histories import create_order_history
from functions.orders import update_order_stage
from functions.stages import one_stage
from functions.users import  add_user_balance
from models.order_done_products import Order_done_products
from models.orders import Orders
from models.stages import Stages
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_order_done_products(order_id, stage_id, from_date, to_date, page, limit, db):
    order_done_products = db.query(Order_done_products).options(
        joinedload(Order_done_products.order), joinedload(Order_done_products.stage),
        joinedload(Order_done_products.user))
    if order_id:
        order_done_products = order_done_products.filter(Order_done_products.order_id == order_id)
    elif stage_id:
        order_done_products = order_done_products.filter(Order_done_products.stage_id == stage_id)
    elif from_date and to_date:
        order_done_products = order_done_products.filter(and_(Order_done_products.date >= from_date, Order_done_products.date <= to_date))

    order_done_products = order_done_products.order_by(Order_done_products.id.desc())
    return pagination(order_done_products, page, limit)


def one_order_done_product(ident, db):
    the_item = db.query(Order_done_products).options(
        joinedload(Order_done_products.order), joinedload(Order_done_products.stage),
        joinedload(Order_done_products.user)).filter(Order_done_products.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order_done_product(form, thisuser, db):
    the_one(db, Orders, form.order_id)
    the_one(db, Stages, form.stage_id)
    new_order_h_db = Order_done_products(
        order_id=form.order_id,
        datetime=date.today(),
        stage_id=form.stage_id,
        worker_id=form.worker_id,
        quantity=form.quantity,
        user_id=thisuser.id,

    )
    save_in_db(db, new_order_h_db)
    stage = one_stage(id=form.stage_id, db=db)
    money = form.quantity * stage.kpi
    create_order_history(order_id=form.order_id, stage_id=form.stage_id, kpi_money=money, thisuser=form.worker_id, db=db)
    add_user_balance(user_id=form.worker_id, money=money, db=db)
    update_order_stage(order_id=form.order_id,stage_id=form.stage_id,db=db)


def update_order_done_product(form, db, thisuser):
    the_one(db, Order_done_products, form.id)
    the_one(db, Orders, form.order_id)
    the_one(db, Stages, form.stage_id)
    db.query(Order_done_products).filter(Order_done_products.id == form.id).update({
        Order_done_products.order_id: form.order_id,
        Order_done_products.date: date.today(),
        Order_done_products.stage_id: form.stage_id,
        Order_done_products.quantity: form.quantity,
        Order_done_products.user_id: thisuser.id
    })
    db.commit()
