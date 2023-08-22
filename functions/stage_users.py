from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.stages import Stages
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.stage_users import Stage_users


def all_stage_user(search,stage_user_id, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Stage_users.name.like(search_formatted)
    else:
        search_filter = Stage_users.id > 0
    
    if stage_user_id:
        search_stage_user_id= Stage_users.stage_id==stage_user_id
    else:
        search_stage_user_id = Stage_users.stage_id>0
    
    stage_user = db.query(Stage_users).options(
        joinedload(Stage_users.stage),
        joinedload(Stage_users.connected_user)).filter(search_filter,search_stage_user_id).order_by(Stage_users.id.desc())
    if page and limit:
        return pagination(stage_user, page, limit)
    else:
        return stage_user.all()


def one_stage_user(id, db):
    the_item = db.query(Stage_users).options(
        joinedload(Stage_users.stage), joinedload(Stage_users.connected_user)).filter(Stage_users.id == id).first()
    if not the_item:
        raise HTTPException(status_code=400, detail="bunday malumot bazada yo'q")
    return the_item


def create_stage_user(form, db, thisuser):
    the_one(db=db, model=Stages, id=form.stage_id)

    new_stage_user_db = Stage_users(

        stage_id=form.stage_id,
        crated_user_id=form.crated_user_id,
        user_id=thisuser.id, )
    save_in_db(db, new_stage_user_db)
    return new_stage_user_db


def update_stage_user(form, db, thisuser):
    the_one(db, Stage_users, form.id)
    the_one(db, Stages, form.stage_id)
    db.query(Stage_users).filter(Stage_users.id == form.id).update({
        Stage_users.stage_id: form.stage_id,
        Stage_users.crated_user_id: form.crated_user_id,
        Stage_users.user_id: thisuser.id
    })
    db.commit()
