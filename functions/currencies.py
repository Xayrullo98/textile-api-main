from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.currencies import Currencies


def all_currencies(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Currencies.name.like(search_formatted)
    else:
        search_filter = Currencies.id > 0

    currencies = db.query(Currencies).filter(search_filter).order_by(Currencies.id.desc())
    if page and limit:
        return pagination(currencies, page, limit)
    else:
        return currencies.all()


def create_currencie(form, db, thisuser):
    new_currencie_db = Currencies(
        name=form.name,
        money=form.money,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)
    return new_currencie_db


def update_currencie(form, db, thisuser):
    the_one(db, Currencies, form.id)
    db.query(Currencies).filter(Currencies.id == form.id).update({
        Currencies.name: form.name,
        Currencies.money: form.money,
        Currencies.user_id: thisuser.id
    })
    db.commit()


def one_currency(id, db):
    return db.query(Currencies).options(
        joinedload(Currencies.order)).filter(Currencies.id == id).first()