import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.incomes import one_income, all_incomes, create_income, update_income
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
def get_incomes(id: int = 0,  page: int = 1,
                limit: int = 25, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_income(id, db)
    else:
        return all_incomes(page=page, limit=limit, db=db)


@incomes_router.post('/create')
def income_create(form: CreateIncome,
                  db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_income(form, db, current_user):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@incomes_router.put("/update")
def income_update(form: UpdateIncome, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if update_income(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


