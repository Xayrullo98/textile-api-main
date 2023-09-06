import datetime
from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload

from functions.stages import one_stage
from functions.users import add_user_balance
from models.order_done_products import Order_done_products
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_order_done_products(order_id, stage_id, from_date, to_date, page, limit, db):
    order_done_products = db.query(Order_done_products).options(
        joinedload(Order_done_products.order), joinedload(Order_done_products.stage),
        joinedload(Order_done_products.user))
    order_done_product_stats = db.query(Order_done_products, func.sum(Order_done_products.quantity *
            Order_done_products.kpi_money).label("total_price")).options(joinedload(Order_done_products.stage))

    if order_id:
        order_done_products = order_done_products.filter(Order_done_products.order_id == order_id)
        order_done_product_stats = order_done_product_stats.filter(Order_done_products.order_id == order_id)
    if stage_id:
        order_done_products = order_done_products.filter(Order_done_products.stage_id == stage_id)
        order_done_product_stats = order_done_product_stats.filter(Order_done_products.stage_id == stage_id)
    if from_date and to_date:
        order_done_products = order_done_products.filter(func.date(Order_done_products.datetime).between(from_date, to_date))
        order_done_product_stats = order_done_product_stats.filter(func.date(Order_done_products.datetime).
                                                                   between(from_date, to_date))

    order_done_products = order_done_products.order_by(Order_done_products.id.desc())
    price_data = []
    order_done_product_stats = order_done_product_stats.group_by(Order_done_products.order_id).all()
    for stat in order_done_product_stats:
        price_data.append({"total_price": stat.total_price, "stage": stat.Order_done_products.stage.name})
    return {"data": pagination(order_done_products, page, limit), "price_data": price_data}


def one_order_done_product(ident, db):
    the_item = db.query(Order_done_products).options(
        joinedload(Order_done_products.order), joinedload(Order_done_products.stage),
        joinedload(Order_done_products.user)).filter(Order_done_products.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order_done_product(form, thisuser, db):
    stage = one_stage(id=form.stage_id, db=db)
    done_product = db.query(Order_done_products).filter(Order_done_products.order_id==form.order_id,
                                                        Order_done_products.stage_id==form.stage_id,
                                                        Order_done_products.datetime==datetime.datetime.now().date(),).first()
    if not done_product:

        new_order_h_db = Order_done_products(
            order_id=form.order_id,
            datetime=datetime.datetime.now().date(),
            stage_id=form.stage_id,
            worker_id=form.worker_id,
            quantity=form.quantity,
            kpi_money=stage.kpi,
            user_id=thisuser.id,

        )
        save_in_db(db, new_order_h_db)
    else:
        quantity = done_product.quantity+form.quantity
        db.query(Order_done_products).filter(Order_done_products.order_id == form.order_id,
                                             Order_done_products.stage_id == form.stage_id,
                                             Order_done_products.datetime == datetime.datetime.now().date(), ).update({
            Order_done_products.datetime: datetime.datetime.now().date(),
            Order_done_products.quantity: quantity,

        })
        db.commit()

    money = form.quantity * stage.kpi
    add_user_balance(user_id=form.worker_id, money=money, db=db)



def update_order_done_product(form, db, thisuser):
    the_one(db, Order_done_products, form.id)
    db.query(Order_done_products).filter(Order_done_products.id == form.id).update({
        Order_done_products.datetime: date.today(),
        Order_done_products.quantity: form.quantity,
        Order_done_products.kpi_money: form.kpi_money,
        Order_done_products.user_id: thisuser.id
    })
    db.commit()
