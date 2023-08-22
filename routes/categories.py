import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.categories import create_category, update_category, all_categories
from models.categories import Categories
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.categories import CreateCategory,UpdateCategory
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
categories_router = APIRouter(
    prefix="/categories",
    tags=["Categories operation"]
)

@categories_router.post('/add', )
def add_category_detail(form: CreateCategory, db: Session = Depends(database),current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_category(form=form, thisuser=current_user, db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@categories_router.get('/', status_code=200)
def get_categories(search: str = None,  id: int = 0,  page: int = 1,
                  limit: int = 25, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    # role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return the_one(db=db, model=Categories, id=id, thisuser=current_user)

    else:
        return all_categories(search=search, page=page, limit=limit, db=db, )


@categories_router.put("/update")
def category_detail_update(form: UpdateCategory, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    if update_category(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

