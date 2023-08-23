from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.currencies import Currencies


def all_currencies(search, page, limit, db):
    currencies = db.query(Currencies)
    if search:
        search_formatted = "%{}%".format(search)
        currencies = currencies.name.like(search_formatted)
    else:
        currencies = Currencies.id > 0

    currencies = currencies.order_by(Currencies.id.desc())
    return pagination(currencies, page, limit)


def create_currencie(form, db, thisuser):
    the_one_model_name(db, Currencies, form.name)
    new_currencie_db = Currencies(
        name=form.name,
        money=form.money,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)


def update_currencie(form, db, thisuser):
    the_one_model_name(db, Currencies, form.name)
    the_one(db, Currencies, form.id)
    db.query(Currencies).filter(Currencies.id == form.id).update({
        Currencies.name: form.name,
        Currencies.money: form.money,
        Currencies.user_id: thisuser.id
    })
    db.commit()

