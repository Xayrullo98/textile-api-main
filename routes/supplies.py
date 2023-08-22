import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.supplies import create_supplier, update_supplier, all_supplies
from models.supplies import Supplies
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.supplies import SuppliesCreate,SuppliesUpdate
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
supplies_router = APIRouter(
    prefix="/supplies",
    tags=["Supplies operation"]
)

@supplies_router.post('/add', )
def add_supplie(form: SuppliesCreate, db: Session = Depends(database),current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_supplier(form=form, thisuser=current_user, db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.get('/', status_code=200)
def get_supplies(search: str = None,  id: int = 0,  page: int = 1,
                  limit: int = 25, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return the_one(db, Supplies, id, current_user)

    else:
        return all_supplies(search=search, page=page, limit=limit, db=db, )


@supplies_router.put("/update")
def supplie_update(form: SuppliesUpdate, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    if update_supplier(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


