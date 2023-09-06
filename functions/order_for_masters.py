from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from functions.stages import one_stage
from functions.users import add_user_balance
from models.order_for_masters import Order_for_masters
from models.orders import Orders
from models.stages import Stages
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_order_for_masters(order_id, stage_id, from_date, to_date, page, limit, db):
    order_for_masters = db.query(Order_for_masters).options(
        joinedload(Order_for_masters.order), joinedload(Order_for_masters.stage),
        joinedload(Order_for_masters.user))
    masters_quantity = db.query(Order_for_masters, func.sum(Order_for_masters.quantity).label("total_quantity")
                                ).options(joinedload(Order_for_masters.stage))
    if order_id:
        order_for_masters = order_for_masters.filter(Order_for_masters.order_id == order_id)
        masters_quantity = masters_quantity.filter(Order_for_masters.order_id == order_id)
    if stage_id:
        order_for_masters = order_for_masters.filter(Order_for_masters.stage_id == stage_id)
        masters_quantity = masters_quantity.filter(Order_for_masters.stage_id == stage_id)
    if from_date and to_date:
        order_for_masters = order_for_masters.filter(func.date(Order_for_masters.datetime).between(from_date, to_date))
        masters_quantity = masters_quantity.filter(func.date(Order_for_masters.datetime).between(from_date, to_date))

    order_for_masters = order_for_masters.order_by(Order_for_masters.id.desc())

    quantity_data = []
    masters_quantity = masters_quantity.group_by(Order_for_masters.stage_id).all()
    for master in masters_quantity:
        quantity_data.append({"total_quantity": master.total_quantity, "stage": master.Order_for_masters.stage.name})
    return {"data": pagination(order_for_masters, page, limit), "total_quantity": quantity_data}


def one_order_for_master(ident, db):
    the_item = db.query(Order_for_masters).options(
        joinedload(Order_for_masters.order), joinedload(Order_for_masters.stage),
        joinedload(Order_for_masters.user)).filter(Order_for_masters.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order_for_master(form, thisuser, db):
    the_one(db, Orders, form.order_id)
    the_one(db, Stages, form.stage_id)
    new_order_h_db = Order_for_masters(
        order_id=form.order_id,
        datetime=datetime.now(),
        stage_id=form.stage_id,
        quantity=form.quantity,
        connected_user_id=form.connected_user_id,
        user_id=thisuser.id,

    )

    save_in_db(db, new_order_h_db)
    stage = one_stage(id=form.stage_id, db=db)
    money = form.quantity * stage.kpi

    add_user_balance(user_id=thisuser.id,money=money,db=db)
    # update_order_stage(order_id=form.order_id, stage_id=form.stage_id, db=db)


def update_order_for_master(form, db, thisuser):
    the_one(db, Order_for_masters, form.id)
    the_one(db, Users, form.connected_user_id)
    db.query(Order_for_masters).filter(Order_for_masters.id == form.id).update({
        Order_for_masters.date: datetime.now(),
        Order_for_masters.quantity: form.quantity,
        Order_for_masters.connected_user_id: form.connected_user_id,
        Order_for_masters.user_id: thisuser.id
    })
    db.commit()
