import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from functions.broken_products import one_broken, all_broken_products
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
broken_products_router = APIRouter(
    prefix="/broken_products",
    tags=["Brak products Endpoints"]
)


@broken_products_router.get('/all')
def get_broken_products(id: int = 0, search: str = None, category_id: int = 0,  page: int = 1,
                        limit: int = 25, db: Session = Depends(database),
                        current_user: UserCurrent = Depends(get_current_active_user)
                        ):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_broken(id, db)
    else:
        return all_broken_products(search, category_id, page, limit, db)
