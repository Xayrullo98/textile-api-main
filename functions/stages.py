from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.measures import Measures
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.stages import Stages


def all_stages(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Stages.name.like(search_formatted)
    else:
        search_filter = Stages.id > 0

    stages = db.query(Stages).options(
        joinedload(Stages.category), joinedload(Stages.measure), joinedload(Stages.stage_user)).filter(search_filter).order_by(Stages.id.desc())
    if page and limit:
        return pagination(stages, page, limit)
    else:
        return stages.all()


def one_stage(id, db):
    return db.query(Stages).options(
        joinedload(Stages.category), joinedload(Stages.measure), joinedload(Stages.stage_user)).filter(Stages.id == id).first()


def create_stage(form, db, thisuser):
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
    new_stage_db = Stages(
        name=form.name,
        number=form.number,
        kpi=form.kpi,
        measure_id=form.measure_id,
        category_id=form.category_id,
        user_id=thisuser.id, )
    save_in_db(db, new_stage_db)


def update_stage(form, db, thisuser):
    the_one(db, Stages, form.id, thisuser)
    the_one(db=db, model=Measures, id=form.measure_id, thisuser=thisuser)
    the_one(db=db, model=Categories, id=form.category_id, thisuser=thisuser)
    db.query(Stages).filter(Stages.id == form.id).update({
        Stages.name: form.name,
        Stages.number: form.number,
        Stages.comment: form.comment,
        Stages.kpi: form.kpi,
        Stages.status: form.status,
        Stages.measure_id: form.measure_id,
        Stages.category_id: form.category_id,
        Stages.user_id: thisuser.id
    })
    db.commit()
