import inspect
from typing import List

from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException
from sqlalchemy.orm import Session

from db import database
from functions.uploaded_files import one_file, all_uploaded_files, create_file, update_file
from routes.login import get_current_active_user
from schemes.users import CreateUser
from utils.role_verification import role_verification

uploaded_files_router = APIRouter(
    prefix="/uploaded_files",
    tags=["Uploaded_files Endpoints"]
)


@uploaded_files_router.get("/")
def get_files(search: str = None, id: int = 0, source: str = None, page: int = 1, limit: int = 25,
              db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user),
             ):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id > 0:
        return one_file(id, db)
    return all_uploaded_files(search, source, page, limit, db)


@uploaded_files_router.post("/create")
def upload_files(
        new_files: List[UploadFile] = File(...),
        source: str = Form(...),
        source_id: int = Form(...),
        comment: str = Form(None),
        db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)
        ):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_file(new_files, source, source_id, comment, current_user, db)
    return {"message": f"{len(new_files)} fayl bazaga saqlandi"}


@uploaded_files_router.put("/update")
def file_update(
        new_files: List[UploadFile] = File(...),
        source: str = Form(...),
        source_id: int = Form(...),
        comment: str = Form(None),
        db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)
):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_file(new_files, source, source_id, comment, current_user, db)
    return {"message": f"{len(new_files)} fayl yangilandi"}


# @uploaded_files_router.delete("/delete", description="source_id bo'yicha barcha medialarni o'chirish")
# def delete_files(source_id: int = Form(...), db: Session = Depends(database),
#                  current_user: CreateUser = Depends(get_current_active_user)):
#
#     role_verification(current_user, inspect.currentframe().f_code.co_name)
#     delete_source_files(source_id, db)
#     raise HTTPException(status_code=200, detail='Amaliyot muvaffaqiyatli yakunlandi')
#


