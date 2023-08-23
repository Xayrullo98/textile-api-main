from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.measures import Measures
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.stages import Stages


def all_stages(measure_id, category_id, search, page, limit, db):
    stages = db.query(Stages).options(joinedload(Stages.category),
                                      joinedload(Stages.measure),
                                      joinedload(Stages.stage_user))
    if measure_id:
        stages = stages.filter(Stages.id == measure_id)
    elif category_id:
        stages = stages.filter(Stages.id == category_id)
    if search:
        search_formatted = "%{}%".format(search)
        stages = stages.name.like(search_formatted)
    else:
        stages = Stages.id > 0

    stages = stages.order_by(Stages.id.desc())
    return pagination(stages, page, limit)


def one_stage(id, db):
    the_item = db.query(Stages).options(
        joinedload(Stages.category), joinedload(Stages.measure),
        joinedload(Stages.stage_user)).filter(Stages.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bazada bunday malumot mavjud emas")
    return the_item


def create_stage(form, db, thisuser):
    the_one_model_name(db, Stages, form.name)
    existing_stage = db.query(Stages).filter(and_(Stages.number == form.number, Stages.name == form.name)).first()
    if existing_stage:
        raise HTTPException(status_code=400, detail="Bir xil nom uchun number bir xil bo'laolmaydi")

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
    the_one_model_name(db, Stages, form.name)
    existing_stage = db.query(Stages).filter(and_(Stages.number == form.number, Stages.name == form.name)).first()
    if existing_stage:
        raise HTTPException(status_code=400, detail="Bir xil nom uchun number bir xil bo'laolmaydi")
    the_one(db, Stages, form.id)
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
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
