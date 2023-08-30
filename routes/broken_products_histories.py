import inspect
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from routes.login import get_current_active_user
from schemes.broken_products_histories import CreateBroken_product_history, UpdateBroken_product_history
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
from functions.broken_products_histories import one_broken_p_history, all_broken_products_histories, \
    create_broken_product_history, update_broken_product_history

broken_products_histories_router = APIRouter(
    prefix="/broken_products_histories",
    tags=["Brak products Histories Endpoints"]
)


@broken_products_histories_router.get('/all')
def get_broken_products_histories(id: int = 0, category_id: int = 0, order_id: int = 0, page: int = 1,
                                  limit: int = 25, db: Session = Depends(database),
                                  current_user: UserCurrent = Depends(get_current_active_user)
                                  ):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_broken_p_history(id, db)
    else:
        return all_broken_products_histories(category_id, order_id, page, limit, db)


@broken_products_histories_router.post('/create')
def create_broken_p_histories(form: CreateBroken_product_history, db: Session = Depends(database),
                              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_broken_product_history(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot bajarildi")


@broken_products_histories_router.put('/update')
def update_broken_p_histories(form: UpdateBroken_product_history, db: Session = Depends(database),
                              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_broken_product_history(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot bajarildi")