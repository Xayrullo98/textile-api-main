import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.stage_users import create_stage_user, update_stage_user, all_stage_user, one_stage_user
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.stage_users import CreateStage_user,UpdateStage_user
from db import database

from schemes.users import UserCurrent
stage_users_router = APIRouter(
    prefix="/stage_users",
    tags=["Stage user operation"]
)

@stage_users_router.post('/add', )
def add_stage_user(form: CreateStage_user, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_stage_user(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@stage_users_router.get('/', status_code=200)
def get_stage_users(stage_id: int = 0, search: str = None,  id: int = 0, page: int = 1,
                    limit: int = 25, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_stage_user(id, db)
    else:
        return all_stage_user(stage_id, search=search, page=page, limit=limit, db=db)


@stage_users_router.put("/update")
def stage_user_update(form: UpdateStage_user, db: Session = Depends(database),
                      current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_stage_user(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


