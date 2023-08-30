from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.stages import Stages
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.stage_users import Stage_users


def all_stage_user(stage_id, connected_user_id, search, page, limit, db):
    stage_users_query = db.query(Stage_users).options(
        joinedload(Stage_users.stage), joinedload(Stage_users.connected_user))

    if search:
        search_formatted = f"%{search}%"
        search_filter = Stage_users.name.ilike(search_formatted)
        stage_users_query = stage_users_query.filter(search_filter)
    if connected_user_id:
        stage_users_query = stage_users_query.filter(Stage_users.connected_user_id == connected_user_id)

    if stage_id:
        stage_users_query = stage_users_query.filter(Stage_users.stage_id == stage_id)

    stage_users_query = stage_users_query.order_by(Stage_users.id.desc())

    return pagination(stage_users_query, page, limit)


def one_stage_user(id, db):
    the_item = db.query(Stage_users).options(
        joinedload(Stage_users.stage), joinedload(Stage_users.connected_user)).filter(Stage_users.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_stage_user(stage_id, connected_user_id, thisuser, db):
    the_one(db, Stages, stage_id)
    the_one(db, Users, connected_user_id)
    existing_stage_user = db.query(Stage_users).filter(
        Stage_users.stage_id == stage_id,
        Stage_users.connected_user_id == connected_user_id
    ).first()
    if existing_stage_user:
        raise HTTPException(status_code=400, detail="Bu stage_id uchun bu connected_user_id bog'langan")

    new_stage_user_db = Stage_users(
        stage_id=stage_id,
        connected_user_id=connected_user_id,
        user_id=thisuser.id, )
    save_in_db(db, new_stage_user_db)


def update_stage_user(form, thisuser, db):
    the_one(db, Stage_users, form.id)
    the_one(db, Stages, form.stage_id)
    # existing_stage_user = db.query(Stage_users).filter(
    #     Stage_users.stage_id == form.stage_id,
    # ).first()
    # if existing_stage_user:
    #     raise HTTPException(status_code=400, detail="Bu stage_id uchun bu connected_user_id bog'langan")

    db.query(Stage_users).filter(Stage_users.id == form.id).update({
        Stage_users.stage_id: form.stage_id,
        # Stage_users.connected_user_id: form.connected_user_id,
        Stage_users.user_id: thisuser.id
    })
    db.commit()


def delete_stage_user(stage_id, db):
    the_one(db, Stages, stage_id)
    db.query(Stage_users).filter(Stage_users.stage_id == stage_id).delete()
    db.commit()