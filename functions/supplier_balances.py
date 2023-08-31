from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.supplies import Supplies
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.supplier_balances import Supplier_balance


def all_supplier_balances(search, currencies_id, supplies_id, from_date, to_date, page, limit, db):
    supplier_balances = db.query(Supplier_balance).options(joinedload(Supplier_balance.supply),
                                                           joinedload(Supplier_balance.currency))

    if search:
        search_formatted = "%{}%".format(search)
        supplier_balances = supplier_balances.balance.like(search_formatted)
    if currencies_id:
        supplier_balances = supplier_balances.filter(Supplier_balance.currencies_id == currencies_id)
    if from_date and to_date:
        supplier_balances = supplier_balances.filter(and_(
            Supplier_balance.date >= from_date, Supplier_balance.date <= to_date))
    if supplies_id:
        supplier_balances = supplier_balances.filter(Supplier_balance.supplies_id == supplies_id)

    supplier_balances = supplier_balances.order_by(Supplier_balance.id.desc())
    return pagination(supplier_balances, page, limit)


def one_supplier_balance(id, db):
    return db.query(Supplier_balance).options(joinedload(Supplier_balance.supply),
                                              joinedload(Supplier_balance.currency)).\
        filter(Supplier_balance.id == id).first()


def create_supplier_balance(form, db, thisuser):

    the_one(db=db, model=Supplies, id=form.supplies_id)
    the_one(db=db, model=Currencies, id=form.currencies_id)
    new_supplier_balance_db = Supplier_balance(
        balance=form.balance,
        currencies_id=form.currencies_id,
        supplies_id=form.supplies_id,
        user_id=thisuser.id
    )
    save_in_db(db, new_supplier_balance_db)


def create_supplier_balance_func(balance, currencies_id, supplies_id, db):
    the_one(db, Supplies, supplies_id)
    the_one(db, Currencies, currencies_id)
    new_supplier_balance_db = Supplier_balance(
        balance=balance,
        currencies_id=currencies_id,
        supplies_id=supplies_id,
    )
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


def total_summa(supplier_id, from_date, to_date, db):
    supliers = db.query(Supplies).filter(Supplies.supplier_id == supplier_id).all()
    summa = 0
    for supplier in supliers:

        supplier_balances = db.query(Supplier_balance).filter(and_(
                Supplier_balance.date >= from_date, Supplier_balance.date <= to_date))
        supplier_balance = db.query(Supplier_balance).filter(Supplier_balance.supplies_id == supplier.id).first()
        summa += supplier_balance
    return summa