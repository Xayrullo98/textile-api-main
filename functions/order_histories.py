from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.order_histories import Order_histories
from models.orders import Orders
from models.stages import Stages
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_order_histories(page, limit, db):
    orders_histories = db.query(Order_histories).options(
        joinedload(Order_histories.order), joinedload(Order_histories.stage),
        joinedload(Order_histories.user))

    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")

    orders_histories = orders_histories.order_by(Orders.id.desc())
    return pagination(orders_histories, page, limit)


def one_order_history(ident, db):
    the_item = db.query(Order_histories).options(
        joinedload(Order_histories.order), joinedload(Order_histories.stage),
        joinedload(Order_histories.user)).filter(Order_histories.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order_history(form, db, thisuser):
    the_one(db, Orders, form.order_id, thisuser)
    the_one(db, Stages, form.stage_id, thisuser)
    new_order_h_db = Order_histories(
        order_id=form.order_id,
        date=date.today(),
        stage_id=form.stage_id,
        kpi_money=form.kpi_money,
        user_id=thisuser.id,

    )
    save_in_db(db, new_order_h_db)
    return new_order_h_db


def update_order_history(form, db, thisuser):
    the_one(db, Order_histories, form.id, thisuser)
    the_one(db, Orders, form.order_id, thisuser)
    the_one(db, Stages, form.stage_id, thisuser)
    db.query(Order_histories).filter(Order_histories.id == form.id).update({
        Order_histories.order_id: form.client_id,
        Order_histories.date: date.today(),
        Order_histories.stage_id: form.stage_id,
        Order_histories.kpi_money: form.kpi_money,
        Order_histories.user_id: thisuser.id
    })
    db.commit()
