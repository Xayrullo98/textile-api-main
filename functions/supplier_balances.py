from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.supplies import Supplies
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.supplier_balances import Supplier_balance


def all_supplier_balances(search,supplier_balances_id,supplies_id, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Supplier_balance.balance.like(search_formatted)
    else:
        search_filter = Supplier_balance.id > 0
    
    if supplier_balances_id:
        search_supplier_balances_id = Supplier_balance.supplier_balances_id==supplier_balances_id
    else:
        search_supplier_balances_id = Supplier_balance.supplier_balances_id>0

    if supplies_id:
        search_supplies_id = Supplier_balance.supplies_id == supplies_id
    else:
        search_supplies_id = Supplier_balance.supplies_id > 0

    supplier_balances = db.query(Supplier_balance).options(
        joinedload(Supplier_balance.balance),joinedload(Supplier_balance.supply),joinedload(Supplier_balance.currency)).filter(search_filter,search_supplies_id,search_supplier_balances_id).order_by(Supplier_balance.id.desc())
    if page and limit:
        return pagination(supplier_balances, page, limit)
    else:
        return supplier_balances.all()

def one_supplier_balance(id, db):
    return db.query(Supplier_balance).options(
        joinedload(Supplier_balance.balance),joinedload(Supplier_balance.supply),joinedload(Supplier_balance.currency)).filter(Supplier_balance.id == id).first()

def create_supplier_balance(form, db, thisuser):
    the_one(db=db, model=Supplies, id=form.supplies_id, thisuser=thisuser)
    the_one(db=db, model=Currencies, id=form.currencies_id, thisuser=thisuser)
    new_supplier_balance_db = Supplier_balance(
        balance=form.balance,
        currencies_id=form.currencies_id,
        supplies_id=form.supplies_id,
        user_id=thisuser.id, )
    save_in_db(db, new_supplier_balance_db)


def update_supplier_balance(form, db, thisuser):
    the_one(db, Supplier_balance, form.id, thisuser)
    the_one(db=db, model=Supplies, id=form.supplies_id, thisuser=thisuser)
    the_one(db=db, model=Currencies, id=form.currencies_id, thisuser=thisuser)
    db.query(Supplier_balance).filter(Supplier_balance.id == form.id).update({
        Supplier_balance.supplier_balances_id: form.supplier_balances_id,
        Supplier_balance.supplies_id: form.supplies_id,
        Supplier_balance.balance: form.balance,
        Supplier_balance.user_id: thisuser.id
    })
    db.commit()
