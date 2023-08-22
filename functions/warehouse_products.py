from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.category_details import Category_details
from models.currencies import Currencies
from models.warehouse_products import Warehouse_products
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_warehouse_products(page, limit, db):
    warehouse_products = db.query(Warehouse_products).options(
        joinedload(Warehouse_products.category_detail), joinedload(Warehouse_products.currency))

    if page and limit:
        return pagination(warehouse_products, page, limit)
    else:
        return warehouse_products


def one_warehouse_p(ident, db):
    the_item = db.query(Warehouse_products).options(
        joinedload(Warehouse_products.currency),
        joinedload(Warehouse_products.category_detail)).filter(Warehouse_products.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_warehouse_product(category_detail_id, quantity, price, currency_id, db, thisuser):
    the_one(db, Category_details, category_detail_id, thisuser)
    the_one(db, Currencies, currency_id, thisuser)
    new_w_p_db = Warehouse_products(
        category_detail_id=category_detail_id,
        quantity=quantity,
        price=price,
        currency_id=currency_id,
    )
    save_in_db(db, new_w_p_db)


def update_warehouse_product(form, db, thisuser):
    the_one(db, Warehouse_products, form.id, thisuser)
    the_one(db, Category_details, form.category_detail_id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    db.query(Warehouse_products).filter(Warehouse_products.id == form.id).update({
        Warehouse_products.category_detail_id: form.category_detail_id,
        Warehouse_products.quantity: form.quantity,
        Warehouse_products.price: form.price,
        Warehouse_products.currency_id: form.currency_id
    })
    db.commit()
