import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.warehouse_products import one_warehouse_p, all_warehouse_products, update_warehouse_product
from routes.login import get_current_active_user
from schemes.warehouse_products import UpdateWarehouse_products
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

warehouse_products_router = APIRouter(
    prefix="/warehouse_products",
    tags=["Warehouse products Endpoints"]
)


@warehouse_products_router.get('/all')
def get_warehouse_products(id: int = 0,  page: int = 1,
                           limit: int = 25, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_warehouse_p(id, db)
    else:
        return all_warehouse_products(page=page, limit=limit, db=db)


@warehouse_products_router.put("/update")
def warehouse_product_update(form: UpdateWarehouse_products, db: Session = Depends(database),
                             current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if update_warehouse_product(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


