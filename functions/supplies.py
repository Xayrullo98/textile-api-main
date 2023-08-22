from sqlalchemy.orm import joinedload

from functions.warehouse_products import create_warehouse_product
from models.currencies import Currencies
from models.suppliers import Suppliers
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.supplies import Supplies


def all_supplies(search, detail_id, supplier_id, currency_id, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Supplies.quantity.like(search_formatted) | Supplies.price.like(
            search_formatted) 
    else:
        search_filter = Supplies.id > 0
    
    if detail_id:
        search_detail_id = Supplies.detail_id==detail_id
    else:
        search_detail_id = Supplies.detail_id>0

    if supplier_id:
        search_supplier_id = Supplies.supplier_id == supplier_id
    else:
        search_supplier_id = Supplies.supplier_id > 0

    if currency_id:
        search_currency_id = Supplies.currency_id == currency_id
    else:
        search_currency_id = Supplies.currency_id > 0

    supplies = db.query(Supplies).filter(search_filter,search_supplier_id,search_currency_id,search_detail_id).order_by(
        Supplies.id.desc())
    if page and limit:
        return pagination(supplies, page, limit)
    else:
        return supplies.all()


def one_supply(id, db):
    return db.query(Suppliers).options(
        joinedload(Suppliers.order)).filter(Suppliers.id == id).first()


def create_supply(form, db, thisuser):
    the_one_model_name(model=Supplies, name=form.name, db=db)
    the_one(db=db, model=Suppliers, id=form.supplier_id)
    the_one(db=db, model=Currencies, id=form.currency_id)
    new_supplier_db = Supplies(
        detail_id=form.detail_id,
        quantity=form.quantity,
        price=form.price,
        supplier_id=form.supplier_id,
        currency_id=form.currency_id,
        user_id=thisuser.id, )
    save_in_db(db, new_supplier_db)
    # after created supply, it should be added warehouse_products
    create_warehouse_product(category_detail_id=form.detail_id, quantity=form.quantity,
                             price=form.price, currency_id=form.currency_id)


def update_supply(form, db, thisuser):
    the_one(db=db, model=Suppliers, id=form.supplier_id)
    the_one(db=db, model=Currencies, id=form.currencies_id)
    the_one(db, Supplies, form.id)
    db.query(Supplies).filter(Supplies.id == form.id).update({
        Supplies.detail_id: form.detail_id,
        Supplies.quantity: form.quantity,
        Supplies.price: form.price,
        Supplies.supplier_id: form.supplier_id,
        Supplies.currency_id: form.currency_id,
        Supplies.user_id: thisuser.id
    })
    db.commit()

def delete_supply(id, db, thisuser):
    the_one(db=db, model=Supplies, id=id)

    db.query(Supplies).filter(Supplies.id == id).update({
        Supplies.status: False,
        Supplies.user_id: thisuser.id
    })
    db.commit()
