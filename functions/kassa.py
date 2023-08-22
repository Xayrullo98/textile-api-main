from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.kassa import Kassas
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_kassas(search, page, limit, db):
    kassas = db.query(Kassas).options(joinedload(Kassas.user), joinedload(Kassas.cu))

    if search:
        search_formatted = "%{}%".format(search)
        kassas = kassas.name.like(search_formatted) | kassas.comment.like(search_formatted)
    else:
        kassas = Kassas.id > 0
    if page and limit:
        return pagination(kassas, page, limit)
    else:
        return kassas


def one_kassa(ident, db):
    the_item = db.query(Kassas).options(
        joinedload(Kassas.user), joinedload(Kassas.currency)).filter(Kassas.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bu id dagi ma'lumot bazada mavjud emas")
    return the_item


def create_kassa(form, db, thisuser):
    the_one(db, Currencies, form.currency_id, thisuser)
    new_kassa_db = Kassas(
        name=form.name,
        comment=form.comment,
        currency_id=form.currency_id,
        balance=0,
        user_id=thisuser.id,
    )
    save_in_db(db, new_kassa_db)


def update_kassa(form, db, thisuser):
    the_one(db, Kassas, form.id, thisuser)
    the_one(db, Currencies, form.currency_id, thisuser)
    db.query(Kassas).filter(Kassas.id == form.id).update({
        Kassas.name: form.name,
        Kassas.comment: form.comment,
        Kassas.user_id: thisuser.id,
        Kassas.currency_id: form.currency_id,
    })
    db.commit()
