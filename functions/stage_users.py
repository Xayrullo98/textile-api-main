from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.stages import Stages
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.stage_users import Stage_users


def all_stage_user(stage_id, category_id, search, page, limit, db):
    stage_users = db.query(Stage_users).options(
        joinedload(Stage_users.stage), joinedload(Stage_users.connected_user))
    if search:
        search_formatted = "%{}%".format(search)
        stage_users = stage_users.name.like(search_formatted)
    else:
        stage_users = Stage_users.id > 0
    if stage_id:
        stage_users = stage_users.filter(Stage_users.id == stage_id)
    elif category_id:
        stage_users = stage_users.filter(Stage_users.id == category_id)
    stage_user = stage_users.order_by(Stage_users.id.desc())

    return pagination(stage_user, page, limit)


def one_stage_user(id, db):
    the_item = db.query(Stage_users).options(
        joinedload(Stage_users.stage), joinedload(Stage_users.connected_user)).filter(Stage_users.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_stage_user(form, db, thisuser):
    # the_one_model_name(db, Stage_users, form.name)
    the_one(db=db, model=Stages, id=form.stage_id, )
    new_stage_user_db = Stage_users(
        name=form.name,
        stage_id=form.stage_id,
        connected_user_id=form.connected_user_id,
        user_id=thisuser.id, )
    save_in_db(db, new_stage_user_db)


def update_stage_user(form, db, thisuser):
    the_one(db, Stage_users, form.id)
    the_one(db, Stages, form.stage_id)
    db.query(Stage_users).filter(Stage_users.id == form.id).update({
        Stage_users.stage_id: form.stage_id,
        Stage_users.crated_user_id: form.crated_user_id,
        Stage_users.user_id: thisuser.id
    })
    db.commit()
