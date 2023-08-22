import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.order_histories import one_order_history, all_order_histories, create_order_history, update_order_history
from routes.login import get_current_active_user
from schemes.order_histories import CreateOrder_history, UpdateOrder_history
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

order_histories_router = APIRouter(
    prefix="/order_histories",
    tags=["Order histories Endpoints"]
)


@order_histories_router.get('/all')
def get_order_histories(id: int = 0,  page: int = 1,
                        limit: int = 25, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_order_history(id, db)
    else:
        return all_order_histories(page=page, limit=limit, db=db)


@order_histories_router.post('/create')
def order_history_create(form: CreateOrder_history,
                 db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_order_history(form, db, current_user):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@order_histories_router.put("/update")
def order_history_update(form: UpdateOrder_history, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if update_order_history(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


