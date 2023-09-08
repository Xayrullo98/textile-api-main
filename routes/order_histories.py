# import inspect
# from datetime import date
#
# from fastapi import APIRouter, Depends, Query
# from sqlalchemy.orm import Session
#
# from functions.order_histories import one_order_history, all_order_histories
# from routes.login import get_current_active_user
# from utils.role_verification import role_verification
# from db import database
# from schemes.users import UserCurrent
#
# order_histories_router = APIRouter(
#     prefix="/order_histories",
#     tags=["Order histories Endpoints"]
# )
#
#
# @order_histories_router.get('/all')
# def get_order_histories(id: int = 0,  page: int = 1, order_id: int = 0, stage_id: int = 0,
#                         from_date: date = Query(None), to_date: date = Query(date.today()),
#                         limit: int = 25, db: Session = Depends(database),
#                         current_user: UserCurrent = Depends(get_current_active_user)):
#     role_verification(current_user, inspect.currentframe().f_code.co_name)
#     if id:
#         return one_order_history(id, db)
#     else:
#         return all_order_histories(order_id, stage_id, from_date, to_date,
#                                    page=page, limit=limit, db=db)

