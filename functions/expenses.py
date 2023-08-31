from _decimal import Decimal
from datetime import date
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, Session

from db import SessionLocal
from functions.users import sup_user_balance
from models.currencies import Currencies
from models.expenses import Expenses
from models.kassa import Kassas
from models.orders import Orders
from models.suppliers import Suppliers
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_expenses(currency_id, from_date, to_date, page, limit, db):
    expenses = db.query(Expenses).options(
        joinedload(Expenses.currency), joinedload(Expenses.order_source),
        joinedload(Expenses.kassa), joinedload(Expenses.user))
    if currency_id:
        expenses = expenses.filter(Expenses.id == currency_id)
    if from_date and to_date:
        expenses = expenses.filter(and_(Expenses.date >= from_date, Expenses.date <= to_date))
    expenses = expenses.order_by(Expenses.id.desc())
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
    the_one(db, Currencies, form.currency_id)
    if kassa.currency_id != form.currency_id:
        raise HTTPException(status_code=400, detail="Bu kassaga bu currency_id bilan qo'shib bo'lmaydi")
    if form.source not in ['supplier', 'user', 'expense']:
        raise HTTPException(status_code=404, detail='source error')

    if form.source == "expense":
        if form.money <= kassa.balance:
            new_expense_db = Expenses(
                currency_id=form.currency_id,
                date=date.today(),
                money=form.money,
                source=form.source,
                source_id=0,
                comment=form.comment,
                kassa_id=form.kassa_id,
                user_id=thisuser.id,
            )
            save_in_db(db, new_expense_db)
            db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
                Kassas.balance: Kassas.balance - form.money
            })
            db.commit()

    if (db.query(Users).filter(Users.id == form.source_id).first() and form.source == "user"
        and the_one(db, Users, form.source_id)) or \
        (db.query(Suppliers).filter(Suppliers.id == form.source_id).first()
         and form.source == "supplier" and the_one(db, Suppliers, form.source_id)):

        if form.money <= kassa.balance:
            if form.source == "user":
                sup_user_balance(user_id=form.source_id, money=form.money, db=db)
            new_expense_db = Expenses(
                currency_id=form.currency_id,
                date=date.today(),
                money=form.money,
                source=form.source,
                source_id=form.source_id,
                comment=form.comment,
                kassa_id=form.kassa_id,
                user_id=thisuser.id,
            )
            save_in_db(db, new_expense_db)

            db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
                Kassas.balance: Kassas.balance - form.money
            })
            db.commit()

        else:
            raise HTTPException(status_code=400, detail="Kassada buncha pul mavjud emas!!!")

    else:
        raise HTTPException(status_code=400, detail="Bu source_id dagi malumot bazada topilmadi")


def update_expense(form, db, thisuser):
    if form.source not in ['supplier', 'user', 'expense']:
        raise HTTPException(status_code=404, detail='source error')
    old_expense = the_one(db, Expenses, form.id)
    kassa = the_one(db, Kassas, form.kassa_id)
    if kassa.currency_id != form.currency_id:
        raise HTTPException(status_code=400, detail="Bu kassaga bu currency_id bilan qo'shib bo'lmaydi")
    the_one(db, Orders, form.source_id)
    the_one(db, Currencies, form.currency_id)

    # Check if the expense was created within the last 5 minutes
    creation_time = old_expense.date
    current_time = datetime.now()
    time_difference = current_time - creation_time
    allowed_time_difference = timedelta(minutes=5)

    if time_difference <= allowed_time_difference:
        if kassa.balance >= form.money:
            db.query(Expenses).filter(Expenses.id == form.id).update({
                Expenses.currency_id: form.currency_id,
                Expenses.date: date.today(),
                Expenses.money: form.money,
                Expenses.source: form.source,
                Expenses.source_id: form.source_id,
                Expenses.kassa_id: form.kassa_id,
                Expenses.comment: form.comment,
                Expenses.user_id: thisuser.id
            })

            db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
                Kassas.balance: Kassas.balance - old_expense.money + Decimal(form.money)
            })
            db.commit()

        else:
            raise HTTPException(status_code=400, detail="Kassada buncha pul mavjud emas!!!")

    else:
        raise HTTPException(status_code=400, detail="Expense can only be updated within 5 minutes after creation")


def add_salary_to_workers():
    db: Session = SessionLocal()
    users = db.query(Users).filter(Users.status==True).all()
    for user in users:
        user_balance = user.balance + user.salary
        db.query(Users).filter(Users.id == user.id).update({
            Users.balance: user_balance
        })
        db.commit()
