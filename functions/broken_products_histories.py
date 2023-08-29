from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.broken_products_histories import Broken_product_histories
from models.categories import Categories
from models.orders import Orders
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_broken_products_histories(category_id, order_id, page, limit, db):
    broken_products_histories = db.query(Broken_product_histories).options(
        joinedload(Broken_product_histories.category),
        joinedload(Broken_product_histories.order))

    if category_id:
        broken_products_histories = broken_products_histories.filter(Broken_product_histories.category_id == category_id).all()
    if order_id:
        broken_products_histories = broken_products_histories.filter(Broken_product_histories.order_id == order_id).all()
    return pagination(broken_products_histories, page, limit)


def one_broken_p_history(ident, db):
    the_item = db.query(Broken_product_histories).options(
        joinedload(Broken_product_histories.category), joinedload(Broken_product_histories.order)
    ).filter(Broken_product_histories.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_broken_product_history(form, db):
    the_one(db, Categories, form.category_id)
    the_one(db, Orders, form.order_id)
    new_broken_history_db = Broken_product_histories(
        category_id=form.category_id,
        quantity=form.quantity,
        order_id=form.order_id
    )
    save_in_db(db, new_broken_history_db)


def update_broken_product_history(form, db):
    the_one(db, Broken_product_histories, db)
    the_one(db, Categories, form.category_id)
    the_one(db, Orders, form.order_id)
    db.query(Broken_product_histories).filter(Broken_product_histories.id == form.id).update({
        Broken_product_histories.category_id: form.category_id,
        Broken_product_histories.order_id: form.order_id,
        Broken_product_histories.quantity: form.quantity
    })
    db.commit()

