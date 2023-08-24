from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, delete_phone
from models.phones import Phones
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.suppliers import Suppliers


def all_suppliers(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Suppliers.name.like(search_formatted) | Suppliers.address.like(
            search_formatted) | Suppliers.comment.like(search_formatted)
    else:
        search_filter = Suppliers.id > 0

    suppliers = db.query(Suppliers).options(joinedload(Suppliers.supplier_phones)).filter(search_filter).order_by(
        Suppliers.id.desc())

    return pagination(suppliers, page, limit)


def one_supplier(ident, db):
    the_item = db.query(Suppliers).options(
        joinedload(Suppliers.user), joinedload(Suppliers.supplier_phones)).filter(Suppliers.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bu id dagi ma'lumot bazada mavjud emas")
    return the_item


def create_supplier(form, db, thisuser):
    the_one_model_name(model=Suppliers, name=form.name, db=db)
    new_supplier_db = Suppliers(
        name=form.name,
        address=form.address,
        comment=form.comment,
        user_id=thisuser.id,
    )
    save_in_db(db, new_supplier_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'supplier', new_supplier_db.id, comment, thisuser.id, db, commit=False)

    db.commit()
    return new_supplier_db

def update_supplier(form, db, thisuser):
    the_one(db, Suppliers, form.id)
    db.query(Suppliers).filter(Suppliers.id == form.id).update({
        Suppliers.name: form.name,
        Suppliers.address: form.address,
        Suppliers.comment: form.comment,
        Suppliers.user_id: thisuser.id
    })
    db.commit()
    client_phones = db.query(Phones).filter(Phones.source_id == form.id).all()
    for phone in client_phones:
        delete_phone(id=phone.id, db=db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number=number, source='supplier', source_id=form.id, comment=comment, user_id=thisuser.id,
                     db=db, commit=False)
    db.commit()
