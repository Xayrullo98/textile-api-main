from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.barcodes import Barcodes
from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_barcodes(search, order_id, page, limit, db):
    barcodes = db.query(Barcodes)

    if search:
        search_formatted = "%{}%".format(search)
        barcodes = barcodes.filter(Categories.name.like(search_formatted))
    if order_id:
        barcodes = barcodes.filter(Barcodes.order_id == order_id).all()
    barcodes = barcodes.order_by(Barcodes.id.desc())
    return pagination(barcodes, page, limit)


def one_barcode(ident, db):
    the_item = db.query(Barcodes).filter(Barcodes.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_barcodes(form,current_user,  db):
    the_one(db, Categories, form.order_id)
    broken_product = db.query(Barcodes).filter(Barcodes.order_id == form.order_id).first()
    if broken_product:
        new_quantity = broken_product.quantity + form.quantity
        db.query(Barcodes).filter(Barcodes.order_id == form.order_id).update({
            Barcodes.quantity: new_quantity
        })
        db.commit()
    else:
        new_broken_db = Barcodes(
            order_id=form.order_id,
            stage_id=form.stage_id,
            name=form.name,
            user_id=current_user.id,
        )
        save_in_db(db, new_broken_db)
    #quantity should be substract from cetegory_detail

