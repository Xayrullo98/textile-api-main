from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.measures import Measures


def all_measures(search, page, limit, db):
    measures = db.query(Measures)
    if search:
        search_formatted = "%{}%".format(search)
        measures = measures.name.like(search_formatted)
    else:
        measures = Measures.id > 0

    measures = measures.order_by(Measures.id.desc())
    return pagination(measures, page, limit)


def create_measure(form, db, thisuser):
    the_one_model_name(db, Measures, form.name)
    new_measure_db = Measures(
        name=form.name,
        user_id=thisuser.id, )
    save_in_db(db, new_measure_db)


def update_measure(form, db, thisuser):
    the_one(db, Measures, form.id)
    the_one_model_name(db, Measures, form.name)
    db.query(Measures).filter(Measures.id == form.id).update({
        Measures.name: form.name,
        Measures.user_id: thisuser.id
    })
    db.commit()
