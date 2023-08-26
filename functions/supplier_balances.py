from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.supplies import Supplies
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.supplier_balances import Supplier_balance


def all_supplier_balances(search, currencies_id, supplies_id, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Supplier_balance.balance.like(search_formatted)
    else:
        search_filter = Supplier_balance.id > 0

    if currencies_id:
        search_currencies_id = Supplier_balance.currencies_id == currencies_id
    else:
        search_currencies_id = Supplier_balance.currencies_id > 0

    if supplies_id:
        search_supplies_id = Supplier_balance.supplies_id == supplies_id
    else:
        search_supplies_id = Supplier_balance.supplies_id > 0

    supplier_balances = db.query(Supplier_balance).filter(search_filter, search_supplies_id,
                                                          search_currencies_id).order_by(
        Supplier_balance.id.desc())
    if page and limit:
        return pagination(supplier_balances, page, limit)
    else:
        return supplier_balances.all()


def one_supplier_balance(id, db):
    return db.query(Supplier_balance).options(
        joinedload(Supplier_balance.order)).filter(Supplier_balance.id == id).first()


def create_supplier_balance(form, db, thisuser):
    the_one(db=db, model=Supplies, id=form.supplies_id)
    the_one(db=db, model=Currencies, id=form.currencies_id)
    new_supplier_balance_db = Supplier_balance(
        balance=form.balance,
        currencies_id=form.currencies_id,
        supplies_id=form.supplies_id,
        user_id=thisuser.id, )
    save_in_db(db, new_supplier_balance_db)


def create_supplier_balance_func(balance, currencies_id, supplies_id, db, thisuser):
    new_supplier_balance_db = Supplier_balance(
        balance=balance,
        currencies_id=currencies_id,
        supplies_id=supplies_id,
        user_id=thisuser.id, )
    save_in_db(db, new_supplier_balance_db)


def update_supplier_balance(form, db, thisuser):
    the_one(db, Supplier_balance, form.id)
    the_one(db=db, model=Supplies, id=form.supplies_id, )
    the_one(db=db, model=Currencies, id=form.currencies_id, )
    db.query(Supplier_balance).filter(Supplier_balance.id == form.id).update({
        Supplier_balance.currencies_id: form.currencies_id,
        Supplier_balance.supplies_id: form.supplies_id,
        Supplier_balance.balance: form.balance,
        Supplier_balance.user_id: thisuser.id
    })
    db.commit()
