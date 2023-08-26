import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.supplier_balances import create_supplier_balance, update_supplier_balance, all_supplier_balances, \
    one_supplier_balance
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.supplier_balances import Supplier_balanceCreate, Supplier_balanceUpdate
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent

supplier_balances_router = APIRouter(
    prefix="/supplier_balances",
    tags=["Supplier_balance operation"]
)


@supplier_balances_router.post('/add', )
def add_supplier_balance(form: Supplier_balanceCreate, db: Session = Depends(database),
                        current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)

    create_supplier_balance(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplier_balances_router.get('/', status_code=200)
def get_supplier_balances(search: str = None, id: int = 0, currencies_id: int = 0, supplies_id: int = 0,
                          page: int = 1,
                          limit: int = 25, db: Session = Depends(database),
                          current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_supplier_balance(id, db)

    else:
        return all_supplier_balances(search=search, page=page, limit=limit, db=db,
                                     currencies_id=currencies_id, supplies_id=supplies_id, )


@supplier_balances_router.put("/update")
def supplier_balance_update(form: Supplier_balanceUpdate, db: Session = Depends(database),
                            current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supplier_balance(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
