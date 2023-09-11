import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from functions.barcodes import one_barcode, all_barcodes
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
barcodes_router = APIRouter(
    prefix="/barcodes",
    tags=["Barcodes  Endpoints"]
)


@barcodes_router.get('/all')
def get_barcodes(id: int = 0, search: str = None, order_id: int = 0,  page: int = 1,
                        limit: int = 25, db: Session = Depends(database),
                        current_user: UserCurrent = Depends(get_current_active_user)
                        ):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_barcode(id, db)
    else:
        return all_barcodes(search, order_id, page, limit, db)

