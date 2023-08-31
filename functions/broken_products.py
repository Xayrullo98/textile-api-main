from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.broken_products import Broken_products
from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_broken_products(search, category_id, page, limit, db):
    broken_products = db.query(Broken_products).options(joinedload(Broken_products.category))

    if search:
        search_formatted = "%{}%".format(search)
        broken_products = broken_products.filter(Categories.name.like(search_formatted))
    if category_id:
        broken_products = broken_products.filter(Broken_products.category == category_id).all()
    broken_products = broken_products.order_by(Broken_products.id.desc())
    return pagination(broken_products, page, limit)


def one_broken(ident, db):
    the_item = db.query(Broken_products).options(
        joinedload(Broken_products.category)).filter(Broken_products.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_broken_product(category_id, quantity, db):
    the_one(db, Categories, category_id)
    broken_product = db.query(Broken_products).filter(Broken_products.category_id == category_id).first()
    if broken_product:
        new_quantity = broken_product.quantity + quantity
        db.query(Broken_products).filter(Broken_products.category_id == category_id).update({
            Broken_products.quantity: new_quantity
        })
        db.commit()
    else:
        new_broken_db = Broken_products(
            category_id=category_id,
            quantity=quantity,
        )
        save_in_db(db, new_broken_db)
    #quantity should be substract from cetegory_detail

