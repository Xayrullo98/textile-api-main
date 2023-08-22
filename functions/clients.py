from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.clients import Clients


def all_clients(search, page, limit, db):
    clients = db.query(Clients).options(joinedload(Clients.user), joinedload(Clients.phones))

    if search:
        search_formatted = f"%{search}%"
        clients = clients.filter(Clients.name.like(search_formatted))
    else:
        clients = clients.filter(Clients.id > 0)

    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")

    clients = clients.order_by(Clients.id.desc())

    return pagination(clients, page, limit)


def one_client(ident, db):
    the_item = db.query(Clients).options(
        joinedload(Clients.user), joinedload(Clients.phones)).filter(Clients.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bu id dagi ma'lumot bazada mavjud emas")
    return the_item


def create_client(form, db, thisuser):
    new_client_db = Clients(
        name=form.name,
        comment=form.comment,
        user_id=thisuser.id,
    )
    save_in_db(db, new_client_db)
    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
            raise HTTPException(status_code=400, detail="Bu nomer bazada mavjud")
        else:
            number = i.number
            create_phone(number, 'client', new_client_db.id, comment, thisuser.id, db)
    raise HTTPException(status_code=200, detail=f"{new_client_db.id} + id li mijoz yaratildi")


def update_client(form, db, thisuser):
    the_one(db, Clients, form.id)
    db.query(Clients).filter(Clients.id == form.id).update({
        Clients.name: form.name,
        Clients.comment: form.comment,
        Clients.user_id: thisuser.id
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, number, 'client', form.id, comment, thisuser.id, db)

