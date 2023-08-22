from sqlalchemy.orm import joinedload

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

    suppliers = db.query(Suppliers).filter(search_filter).order_by(
        Suppliers.id.desc())
    if page and limit:
        return pagination(suppliers, page, limit)
    else:
        return suppliers.all()
def one_supplier(id, db):
    return db.query(Suppliers).options(
        joinedload(Suppliers.order)).filter(Suppliers.id == id).first()

def create_supplier(form, db, thisuser):
    the_one_model_name(model=Suppliers, name=form.name, db=db)
    new_supplier_db = Suppliers(
        name=form.name,
        address=form.address,
        comment=form.comment,
        user_id=thisuser.id, )
    save_in_db(db, new_supplier_db)


def update_supplier(form, db, thisuser):
    the_one(db, Suppliers, form.id)
    db.query(Suppliers).filter(Suppliers.id == form.id).update({
        Suppliers.name: form.name,
        Suppliers.address: form.address,
        Suppliers.comment: form.comment,
        Suppliers.user_id: thisuser.id
    })
    db.commit()
