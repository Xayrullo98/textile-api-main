from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.incomes import Incomes
from models.kassa import Kassas
from models.orders import Orders
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_incomes(page, limit, db):
    incomes = db.query(Incomes).options(
        joinedload(Incomes.currency), joinedload(Incomes.order_source),
        joinedload(Incomes.kassa), joinedload(Incomes.user))

    if page and limit:
        return pagination(incomes, page, limit)
    else:
        return incomes


def one_income(ident, db):
    the_item = db.query(Incomes).options(
        joinedload(Incomes.currency), joinedload(Incomes.order_source),
        joinedload(Incomes.user), joinedload(Incomes.kassa)).filter(Incomes.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_income(form, db, thisuser):
    the_one(db, Kassas, form.kassa_id, thisuser)
    the_one(db, Orders, form.source_id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    new_income_db = Incomes(
        currency_id=form.currency_id,
        date=date.now(),
        money=form.money,
        source=form.source,
        source_id=form.source_id,
        comment=form.comment,
        user_id=thisuser.id,
    )
    save_in_db(db, new_income_db)
    return new_income_db


def update_income(form, db, thisuser):
    the_one(db, Incomes, form.id, thisuser)
    the_one(db, Kassas, form.kassa_id, thisuser)
    the_one(db, Orders, form.source_id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    db.query(Incomes).filter(Incomes.id == form.id).update({
        Incomes.currency_id: form.currency_id,
        Incomes.date: date,
        Incomes.money: form.money,
        Incomes.source: form.source,
        Incomes.source_id: form.source_id,
        Incomes.comment: form.comment,
        Incomes.user_id: thisuser.id
    })
    db.commit()


