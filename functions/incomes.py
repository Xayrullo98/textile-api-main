from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.incomes import Incomes
from models.kassa import Kassas
from models.orders import Orders
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_incomes(currency_id, from_date, to_date, page, limit, db):
    incomes = db.query(Incomes).options(
        joinedload(Incomes.currency), joinedload(Incomes.order_source),
        joinedload(Incomes.kassa), joinedload(Incomes.user))
    if currency_id:
        incomes = incomes.filter(Incomes.id == currency_id)
    elif from_date and to_date:
        incomes = incomes.filter(and_(Incomes.date >= from_date, Incomes.date <= to_date))

    return pagination(incomes, page, limit)


def one_income(ident, db):
    the_item = db.query(Incomes).options(
        joinedload(Incomes.currency), joinedload(Incomes.order_source),
        joinedload(Incomes.user), joinedload(Incomes.kassa)).filter(Incomes.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_income(form, db, thisuser):
    if form.source not in ['order']:
        raise HTTPException(status_code=400, detail='source error')
    kassa = the_one(db, Kassas, form.kassa_id)
    if kassa.currency_id != form.currency_id:
        raise HTTPException(status_code=400, detail="Bu kassaga bu currency_id bilan qo'shib bo'lmaydi")

    the_one(db, Orders, form.source_id)
    the_one(db, Currencies, form.currency_id)
    new_income_db = Incomes(
        currency_id=form.currency_id,
        date=date.today(),
        money=form.money,
        source=form.source,
        source_id=form.source_id,
        kassa_id=form.kassa_id,
        comment=form.comment,
        user_id=thisuser.id,
    )
    save_in_db(db, new_income_db)
    db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
        Kassas.balance: Kassas.balance + form.money
    })
    db.commit()


def update_income(form, db, thisuser):
    if form.source not in ['order']:
        raise HTTPException(status_code=400, detail='source error')
    old_income = the_one(db, Incomes, form.id)
    the_one(db, Orders, form.source_id)
    the_one(db, Currencies, form.currency_id)
    kassa = the_one(db, Kassas, form.kassa_id)
    if kassa.currency_id != form.currency_id:
        raise HTTPException(status_code=400, detail="Bu kassaga bu currency_id bilan qo'shib bo'lmaydi")

    kassa_balance = kassa.balance - old_income.money + form.money
    db.query(Incomes).filter(Incomes.id == form.id).update({
        Incomes.currency_id: form.currency_id,
        Incomes.date: date.today(),
        Incomes.money: form.money,
        Incomes.source: form.source,
        Incomes.source_id: form.source_id,
        Incomes.kassa_id: form.kassa_id,
        Incomes.comment: form.comment,
        Incomes.user_id: thisuser.id
    })
    db.commit()
    db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
        Kassas.balance: Kassas.balance + kassa_balance
    })
    db.commit()



