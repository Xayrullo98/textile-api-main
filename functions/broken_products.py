from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.broken_products import Broken_products
from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.clients import Clients


def all_broken_products(page, limit, db):
    broken_products = db.query(Broken_products).options(joinedload(Broken_products.category))

    if page and limit:
        return pagination(broken_products, page, limit)
    else:
        return broken_products


def one_broken(ident, db):
    the_item = db.query(Broken_products).options(
        joinedload(Broken_products.category)).filter(Clients.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_broken_product(form, db, thisuser):
    the_one(db, Categories, form.category_id, thisuser)
    new_broken_db = Broken_products(
        category_id=form.category_id,
        quantity=form.quantity,
    )
    save_in_db(db, new_broken_db)
    #quantity should be substract from cetegory_detail



def update_broken(form, db, thisuser):
    the_one(db, Categories, form.category_id, thisuser)
    the_one(db, Broken_products, form.id, thisuser)
    db.query(Broken_products).filter(Broken_products.id == form.id).update({
        Broken_products.category_id: form.category_id,
        Broken_products.quantity: form.quantity,
    })
    db.commit()
