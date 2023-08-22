from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.measures import Measures


def all_measures(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Measures.name.like(search_formatted)
    else:
        search_filter = Measures.id > 0

    measures = db.query(Measures).options(
        joinedload(Measures.stage), joinedload(Measures.category_detail)).filter(search_filter).filter(
        search_filter).order_by(Measures.id.desc())
    if page and limit:
        return pagination(measures, page, limit)
    else:
        return measures.all()


def one_measure(id, db):
    return db.query(Measures).options(
        joinedload(Measures.stage), joinedload(Measures.category_detail)).filter(Measures.id == id).first()


def create_measure(form, db, thisuser):
    new_measure_db = Measures(
        name=form.name,
        user_id=thisuser.id, )
    save_in_db(db, new_measure_db)


def update_measure(form, db, thisuser):
    the_one(db, Measures, form.id, thisuser)
    db.query(Measures).filter(Measures.id == form.id).update({
        Measures.name: form.name,
        Measures.user_id: thisuser.id
    })
    db.commit()
