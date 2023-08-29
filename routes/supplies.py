import inspect
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.supplies import create_supply, update_supply, all_supplies, delete_supply, one_supply, supply_confirm

from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.supplies import SuppliesCreate, SuppliesUpdate, SuppliesConfirm, SuppliesUpdateConfirm
from db import database

from schemes.users import UserCurrent
supplies_router = APIRouter(
    prefix="/supplies",
    tags=["Supplies operation"]
)


@supplies_router.post('/add')
def add_supplie(form: SuppliesCreate, db: Session = Depends(database),current_user:
                UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_supply(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


#check warehouse products
@supplies_router.get('/', status_code=200)
def get_supplies(search: str = None,  id: int = 0,
                 category_detail_id: int = 0, supplier_id: int = 0,
                 currency_id:int=0, status: bool = None, page: int = 1,
                 limit: int = 25, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_supply(id, db)

    else:
        return all_supplies(search=search, category_detail_id=category_detail_id,
                            supplier_id=supplier_id, currency_id=currency_id, status=status, page=page, limit=limit, db=db)


@supplies_router.put("/update")
def supply_update(form: SuppliesUpdate, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supply(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.post("/confirm")
def confirm_supply(form:SuppliesUpdateConfirm, db: Session = Depends(database),
                  current_user:  UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    for data in form.ids:

        supply_confirm(data.id, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

@supplies_router.delete("/delete")
def supply_delete(id: int, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_supply(id, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")