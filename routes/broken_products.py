import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.broken_products import one_broken, all_broken_products, create_broken_product, update_broken
from routes.login import get_current_active_user
from schemes.broken_products import CreateBroken_product, UpdateBroken_product
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
broken_products_router = APIRouter(
    prefix="/broken_products",
    tags=["Brak products Endpoints"]
)


@broken_products_router.get('/all', status_code=200)
def get_broken_products(id: int = 0,  page: int = 1,
                        limit: int = 25, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_broken(id, db)
    else:
        return all_broken_products(page=page, limit=limit, db=db)


@broken_products_router.post('/create')
def broken_create(form: CreateBroken_product, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_broken_product(form=form, thisuser=current_user, db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@broken_products_router.put("/update")
def broken_update(form: UpdateBroken_product, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if update_broken(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


