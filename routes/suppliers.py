import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.suppliers import create_supplier, update_supplier, all_suppliers, one_supplier
from models.suppliers import Suppliers
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.suppliers import SuppliersCreate,SuppliersUpdate
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
suppliers_router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers operation"]
)

@suppliers_router.post('/add', )
def add_category_detail(form: SuppliersCreate, db: Session = Depends(database),
                        current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_supplier(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@suppliers_router.get('/', status_code=200)
def get_suppliers(search: str = None,  id: int = 0,  page: int = 1,
                  limit: int = 25, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_supplier(id, db)
    else:
        return all_suppliers(search=search, page=page, limit=limit, db=db, )


@suppliers_router.put("/update")
def category_detail_update(form: SuppliersUpdate, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supplier(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


