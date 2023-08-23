from _decimal import Decimal
from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.expenses import Expenses
from models.kassa import Kassas
from models.orders import Orders
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_expenses(currency_id, from_date, to_date, page, limit, db):
    expenses = db.query(Expenses).options(
        joinedload(Expenses.currency), joinedload(Expenses.order_source),
        joinedload(Expenses.kassa), joinedload(Expenses.user))
    if currency_id:
        expenses = expenses.filter(Expenses.id == currency_id)
    elif from_date and to_date:
        expenses = expenses.filter(and_(Expenses.date >= from_date, Expenses.date <= to_date))

    return pagination(expenses, page, limit)


def one_expense(ident, db):
    the_item = db.query(Expenses).options(
        joinedload(Expenses.currency), joinedload(Expenses.order_source),
        joinedload(Expenses.user), joinedload(Expenses.kassa)).filter(Expenses.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_expense(form, db, thisuser):
    kassa = the_one(db, Kassas, form.kassa_id)
    the_one(db, Orders, form.source_id)
    the_one(db, Currencies, form.currency_id)
    if form.source not in ['supplier', 'user', 'expense']:
        raise HTTPException(status_code=404, detail='source error')
    if form.money <= kassa.balance:
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
            Kassas.balance: Kassas.balance - form.money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Kassada buncha pul mavjud emas!!!")


def update_expense(form, db, thisuser):
    if form.source not in ['supplier', 'user', 'expence']:
        raise HTTPException(status_code=404, detail='source error')
    old_expense = the_one(db, Expenses, form.id)
    kassa = the_one(db, Kassas, form.kassa_id)
    the_one(db, Orders, form.source_id)
    the_one(db, Currencies, form.currency_id)
    # agar kassada yetarli pul mavjud bo'lsa kassadan ayiramiz, aks holda xatolik chiqaaradi
    if kassa.balance >= form.money:
        db.query(Expenses).filter(Expenses.id == form.id).update({
            Expenses.currency_id: form.currency_id,
            Expenses.date: date.today(),
            Expenses.money: form.money,
            Expenses.source: form.source,
            Expenses.source_id: form.source_id,
            Expenses.comment: form.comment,
            Expenses.user_id: thisuser.id
        })

        db.query(Kassas).filter(Kassas.id == form.id).update({
            Kassas.balance: Kassas.balance - old_expense.money + Decimal(form.money)
        })
        db.commit()

    else:
        raise HTTPException(status_code=400, detail="Kassada buncha pul mavjud emas!!!")




