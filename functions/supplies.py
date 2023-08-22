from sqlalchemy.orm import joinedload

from functions.warehouse_products import create_warehouse_product
from models.currencies import Currencies 
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.supplies import Supplies


def all_supplies(search, detail_id, supply_id, currency_id, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Supplies.quantity.like(search_formatted) | Supplies.price.like(
            search_formatted)
    else:
        search_filter = Supplies.id > 0

    if detail_id:
        search_detail_id = Supplies.detail_id == detail_id
    else:
        search_detail_id = Supplies.detail_id > 0

    if supply_id:
        search_supply_id = Supplies.supply_id == supply_id
    else:
        search_supply_id = Supplies.supply_id > 0

    if currency_id:
        search_currency_id = Supplies.currency_id == currency_id
    else:
        search_currency_id = Supplies.currency_id > 0

    supplies = db.query(Supplies).filter(search_filter, search_supply_id, search_currency_id,
                                         search_detail_id).order_by(
        Supplies.id.desc())
    if page and limit:
        return pagination(supplies, page, limit)
    else:
        return supplies.all()


def one_supplies(id, db):
    return db.query(Supplies).options(
        joinedload(Supplies.order)).filter(Supplies.id == id).first()


def create_supply(form, db, thisuser):
    the_one(db=db, model=Supplies, id=form.supply_id, thisuser=thisuser)
    the_one(db=db, model=Currencies, id=form.currencies_id, thisuser=thisuser)
    new_supply_db = Supplies(
        detail_id=form.detail_id,
        quantity=form.quantity,
        price=form.price,
        supply_id=form.supply_id,
        currency_id=form.currency_id,
        user_id=thisuser.id, )
    save_in_db(db, new_supply_db)

    # after created supply, it should be added warehouse_products
    create_warehouse_product(category_detail_id=form.detail_id, quantity=form.quantity,
                             price=form.price, currency_id=form.currency_id, db=db, thisuser=thisuser)


def update_supply(form, db, thisuser):
    the_one(db=db, model=Supplies, id=form.supply_id, thisuser=thisuser)
    the_one(db=db, model=Currencies, id=form.currencies_id, thisuser=thisuser)
    the_one(db, Supplies, form.id, thisuser)
    db.query(Supplies).filter(Supplies.id == form.id).update({
        Supplies.detail_id: form.detail_id,
        Supplies.quantity: form.quantity,
        Supplies.price: form.price,
        Supplies.supply_id: form.supply_id,
        Supplies.currency_id: form.currency_id,
        Supplies.user_id: thisuser.id
    })
    db.commit()
