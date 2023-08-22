import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.currencies import create_currencie, update_currencie, all_currencies
from models.currencies import Currencies
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.currencies import CurrenciesCreate,CurrenciesUpdate
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
currencies_router = APIRouter(
    prefix="/currencies",
    tags=["Currencies operation"]
)

@currencies_router.post('/add', )
def add_category_detail(form: CurrenciesCreate, db: Session = Depends(database),current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_currencie(form=form, thisuser=current_user, db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@currencies_router.get('/', status_code=200)
def get_currencies(search: str = None,  id: int = 0,  page: int = 1,
                  limit: int = 25, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return the_one(db, Currencies, id, current_user)

    else:
        return all_currencies(search=search, page=page, limit=limit, db=db, )


@currencies_router.put("/update")
def category_detail_update(form: CurrenciesUpdate, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    if update_currencie(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

