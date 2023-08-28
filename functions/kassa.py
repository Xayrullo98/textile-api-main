from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, delete_phone
from models.currencies import Currencies
from models.kassa import Kassas
from models.phones import Phones
from utils.db_operations import  the_one, the_one_model_name
from utils.pagination import pagination


def all_kassas(currency_id, search, page, limit, db):
    kassas = db.query(Kassas).options(joinedload(Kassas.user), joinedload(Kassas.currency), joinedload(Kassas.kassa_phones))

    if search:
        search_formatted = f"%{search}%"
        kassas = kassas.filter(
            (Kassas.name.like(search_formatted)) |
            (Kassas.comment.like(search_formatted)))
    if currency_id:
        kassas = kassas.filter(Kassas.currency_id == currency_id)
    kassas = kassas.order_by(Kassas.id.desc())
    return pagination(kassas, page, limit)


def one_kassa(ident, db):
    the_item = db.query(Kassas).options(
        joinedload(Kassas.user), joinedload(Kassas.currency),
        joinedload(Kassas.kassa_phones)
    ).filter(Kassas.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bu id dagi ma'lumot bazada mavjud emas")
    return the_item


def create_kassa(form, db, thisuser):
    the_one(db, Currencies, form.currency_id)
    the_one_model_name(db, Kassas, form.name)
    new_kassa_db = Kassas(
        name=form.name,
        comment=form.comment,
        currency_id=form.currency_id,
        balance=0,
        user_id=thisuser.id,
    )
    db.add(new_kassa_db)
    db.flush()
    #kassa uchun phone number yaratish
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'kassa', new_kassa_db.id, comment, thisuser.id, db, commit=False)

    db.commit()
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli bajarildi")


def update_kassa(form, thisuser,  db):
    the_one(db, Kassas, form.id)
    the_one_model_name(db, Kassas, form.name)
    db.query(Kassas).filter(Kassas.id == form.id).update({
        Kassas.name: form.name,
        Kassas.comment: form.comment,
        Kassas.user_id: thisuser.id,
    })

    #kassani phone_numberini yangilash
    kassa_phones = db.query(Phones).filter(Phones.source_id == form.id).all()
    for phone in kassa_phones:
        delete_phone(id=phone.id, db=db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number=number, source='kassa', source_id=form.id, comment=comment, user_id=thisuser.id,
                         db=db,  commit=False)
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


