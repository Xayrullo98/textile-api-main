import inspect
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from functions.order_done_products import create_order_done_product, update_order_done_product,\
    all_order_done_products, one_order_done_product
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.order_done_products import CreateOrder_done_products, UpdateOrder_done_products
from db import database

from schemes.users import UserCurrent
order_done_products_router = APIRouter(
    prefix="/order_done_products",
    tags=["Order done products operation"]
)


@order_done_products_router.post('/add', )
def add_stage_user(form: CreateOrder_done_products, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_order_done_product(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@order_done_products_router.get('/', status_code=200)
def get_order_done_products(stage_id: int = 0, order_id: int = 0,worker_id: int = 0,  id: int = 0, page: int = 1,
                    from_date: date = Query(None), to_date: date = Query(date.today()),
                    limit: int = 25, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_order_done_product(id, db)
    else:
        return all_order_done_products(stage_id=stage_id, order_id=order_id,worker_id=worker_id, page=page, limit=limit, db=db,from_date=from_date,to_date=to_date)


@order_done_products_router.put("/update")
def stage_user_update(form: UpdateOrder_done_products, db: Session = Depends(database),
                      current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_order_done_product(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

