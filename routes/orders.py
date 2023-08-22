import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.orders import one_order, all_orders, create_order, update_order
from routes.login import get_current_active_user
from schemes.orders import CreateOrder, UpdateOrder
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders Endpoints"]
)


@orders_router.get('/all')
def get_orders(id: int = 0,  page: int = 1,
                           limit: int = 25, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_order(id, db)
    else:
        return all_orders(page=page, limit=limit, db=db)


@orders_router.post('/create')
def order_create(form: CreateOrder,
                 db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_order(form, db, current_user):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@orders_router.put("/update")
def order_update(form: UpdateOrder, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if update_order(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


