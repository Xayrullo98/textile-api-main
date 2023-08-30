from datetime import datetime, date
import inspect


from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from functions.incomes import one_income, all_incomes, create_income, update_income, calculate_sum_of_money
from routes.login import get_current_active_user
from schemes.incomes import CreateIncome, UpdateIncome
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

incomes_router = APIRouter(
    prefix="/incomes",
    tags=["Incomes Endpoints"]
)


@incomes_router.get('/all')
def get_incomes(id: int = 0, currency_id: int = 0,
                from_date: date = Query('2023-08-29'), to_date: date = Query(datetime.today()),  page: int = 1,
                limit: int = 25, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_income(id, db)
    else:
        return all_incomes( currency_id, from_date, to_date, page=page, limit=limit, db=db)


@incomes_router.get("/summa")
def calculate_summa(
        kassa_id: int,
        from_date: date = Query("2023-08-29"),
        to_date: date = Query(date.today()),
        db: Session = Depends(database),
        current_user: UserCurrent = Depends(get_current_active_user)
        ):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    total_sum = calculate_sum_of_money(kassa_id, from_date, to_date, db)
    return {"total_sum": total_sum}