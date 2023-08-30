import inspect
from datetime import date, datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from functions.supplier_balances import create_supplier_balance, update_supplier_balance, all_supplier_balances, \
    one_supplier_balance, total_summa
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


@supplier_balances_router.get('/', status_code=200)
def get_supplier_balances(search: str = None, id: int = 0, currencies_id: int = 0, supplies_id: int = 0,
                          page: int = 1, from_date: date = Query("2023-08-28"),
                          to_date: date = Query(datetime.today()),
                          limit: int = 25, db: Session = Depends(database),
                          current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_supplier_balance(id, db)

    else:
        return all_supplier_balances(search, currencies_id, supplies_id,
                                     from_date, to_date, page, limit, db)


@supplier_balances_router.get('/summa')
def calculate_balance(supplier_id: int = 0, from_date: date = Query("2023-08-28"), to_date: date = Query(datetime.today()),
                      db: Session = Depends(database),
                      current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    total_summa(supplier_id, from_date, to_date, db)
