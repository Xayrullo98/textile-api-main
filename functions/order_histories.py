from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from models.order_histories import Order_histories
from models.orders import Orders
from models.stages import Stages
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_order_histories(order_id, stage_id, from_date, to_date, page, limit, db):
    order_histories = db.query(Order_histories).options(
        joinedload(Order_histories.order), joinedload(Order_histories.stage),
        joinedload(Order_histories.user))
    if order_id:
        order_histories = order_histories.filter(Order_histories.id == order_id)
    if stage_id:
        order_histories = order_histories.filter(Order_histories.id == stage_id)
    if from_date and to_date:
        order_histories = order_histories.filter(and_(Order_histories.date >= from_date, Order_histories.date <= to_date))

    order_histories = order_histories.order_by(Order_histories.id.desc())
    return pagination(order_histories, page, limit)


def one_order_history(ident, db):
    the_item = db.query(Order_histories).options(
        joinedload(Order_histories.order), joinedload(Order_histories.stage),
        joinedload(Order_histories.user)).filter(Order_histories.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order_history(order_id, stage_id, kpi_money, thisuser, db):
    the_one(db, Orders, order_id)
    the_one(db, Stages, stage_id)

    if str(thisuser).isdigit():

        new_order_h_db = Order_histories(
            order_id=order_id,
            date=date.today(),
            stage_id=stage_id,
            kpi_money=kpi_money,
            user_id=thisuser,
        )
        save_in_db(db, new_order_h_db)
    else:
        new_order_h_db = Order_histories(
            order_id=order_id,
            date=date.today(),
            stage_id=stage_id,
            kpi_money=kpi_money,
            user_id=thisuser.id,
        )

        save_in_db(db, new_order_h_db)


def update_order_history(id, order_id, stage_id, kpi_money, db, thisuser):
    the_one(db, Order_histories, id)
    the_one(db, Orders, order_id)
    the_one(db, Stages, stage_id)
    db.query(Order_histories).filter(Order_histories.id == id).update({
        Order_histories.order_id: order_id,
        Order_histories.date: date.today(),
        Order_histories.stage_id: stage_id,
        Order_histories.kpi_money: kpi_money,
        Order_histories.user_id: thisuser.id
    })
    db.commit()
