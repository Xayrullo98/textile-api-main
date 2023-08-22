from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.expenses import Expenses
from models.kassa import Kassas
from models.orders import Orders
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_expenses(page, limit, db):
    expenses = db.query(Expenses).options(
        joinedload(Expenses.currency), joinedload(Expenses.order_source),
        joinedload(Expenses.kassa), joinedload(Expenses.user))

    if page and limit:
        return pagination(expenses, page, limit)
    else:
        return expenses


def one_expense(ident, db):
    the_item = db.query(Expenses).options(
        joinedload(Expenses.currency), joinedload(Expenses.order_source),
        joinedload(Expenses.user), joinedload(Expenses.kassa)).filter(Expenses.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_expense(form, db, thisuser):
    the_one(db, Kassas, form.kassa_id, thisuser)
    the_one(db, Orders, form.source_id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    new_expense_db = Expenses(
        currency_id=form.currency_id,
        date=date.now(),
        money=form.money,
        source=form.source,
        source_id=form.source_id,
        comment=form.comment,
        user_id=thisuser.id,
    )
    save_in_db(db, new_expense_db)
    db.query(Kassas).filter(Kassas.id == form.id).update({
        Kassas.balance: Kassas.balance - form.money()
    })
    db.commit()


def update_expense(form, db, thisuser):
    the_one(db, Expenses, form.id, thisuser)
    the_one(db, Kassas, form.kassa_id, thisuser)
    the_one(db, Orders, form.source_id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    db.query(Expenses).filter(Expenses.id == form.id).update({
        Expenses.currency_id: form.currency_id,
        Expenses.date: date,
        Expenses.money: form.money,
        Expenses.source: form.source,
        Expenses.source_id: form.source_id,
        Expenses.comment: form.comment,
        Expenses.user_id: thisuser.id
    })
    db.commit()

