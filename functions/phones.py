from fastapi import HTTPException

from utils.db_operations import save_in_db
from utils.pagination import pagination
from models.phones import Phones


def all_phones(search, page, limit, db, branch_id):
    phones = db.query(Phones)
    if search:
        search_formatted = f"%{search}%"
        phones = phones.filter(Phones.source.like(search_formatted))
    else:
        phones = Phones.id > 0
    phones = phones.order_by(Phones.id.desc())
    return pagination(phones, page, limit)


def create_phone(number, source, source_id, comment, user_id, db, commit=True):
    if db.query(Phones).filter(Phones.number == number, Phones.source == source).first():
        raise HTTPException(status_code=400, detail="Bu nomer bazada mavjud")
    new_phone_db = Phones(
        number=number,
        comment=comment,
        source=source,
        source_id=source_id,
        user_id=user_id
    )
    db.add(new_phone_db)

    if commit:
        db.commit()


def update_phone(phone_id, number, source, source_id, comment, user_id, db,  commit=True):
    if db.query(Phones).filter(Phones.number == number, Phones.source == source).first():
        raise HTTPException(status_code=400, detail="Bu nomer bazada mavjud")
    db.query(Phones).filter(Phones.id == phone_id).update({
        Phones.number: number,
        Phones.comment: comment,
        Phones.source: source,
        Phones.source_id: source_id,
        Phones.user_id: user_id
    })
    if commit:
        db.commit()


def delete_phone(id, db):
    db.query(Phones).filter(Phones.id == id).delete()
    db.commit()

