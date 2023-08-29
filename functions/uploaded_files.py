import os
from typing import List

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.uploaded_files import Uploaded_files

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_uploaded_files(search, source, page, limit, db):
    uploaded = db.query(Uploaded_files).options(joinedload(Uploaded_files.user),
                                          joinedload(Uploaded_files.category_source).load_only(Categories.name))
    if source:
        uploaded = uploaded.filter(Uploaded_files.source == source)
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = uploaded.filter(Uploaded_files.comment.like(search_formatted))
    else:
        search_filter = Uploaded_files.id > 0
    uploaded = uploaded.filter(search_filter).order_by(Uploaded_files.id.desc())
    return pagination(uploaded, page, limit)


def one_file(ident, db):
    the_item = db.query(Uploaded_files).filter(Uploaded_files.id == ident).options(
        joinedload(Uploaded_files.user), joinedload(Uploaded_files.category).load_only(Categories.name)).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail=f"Bazada bunday ma'lumot mavjud emas")
    return the_item


def create_file(new_files, source, source_id, comment, thisuser, db):
    if source not in ['category']:
        raise HTTPException(status_code=400, detail="Source error")
    the_one(db, Categories, source_id)
    if db.query(Categories).filter(Categories.id == source_id).first() and source == "category":
        uploaded_file_objects = []

        for new_file in new_files:
            file_location = f"Uploaded_files/{new_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(new_file.file.read())

            new_file_db = Uploaded_files(
                file=file_location,
                source=source,
                source_id=source_id,
                comment=comment,
                user_id=thisuser.id,
            )
            uploaded_file_objects.append(new_file_db)

        db.add_all(uploaded_file_objects)
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source va source_id bir biriga to'g'ri kelmadi")


def delete_file(id, db):
    file = the_one(db, Uploaded_files, id)
    db.query(Uploaded_files).filter(Uploaded_files.id == id).delete()
    os.unlink(file.file)
    db.commit()


def update_file(new_files, source, source_id, comment, thisuser, db):

    if source not in ['category']:
        raise HTTPException(status_code=400, detail="Source error")
    the_one(db, Categories, source_id)
    update_files = db.query(Uploaded_files).filter(Uploaded_files.source_id == source_id).all()
    for file in update_files:
        delete_file(file.id, db)

    if db.query(Categories).filter(Categories.id == source_id).first() and source == "category":
        uploaded_file_objects = []

        for new_file in new_files:

            file_location = f"Uploaded_files/{new_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(new_file.file.read())

            new_file_db = Uploaded_files(
                file=file_location,
                source=source,
                source_id=source_id,
                comment=comment,
                user_id=thisuser.id,
            )
            uploaded_file_objects.append(new_file_db)

        db.add_all(uploaded_file_objects)
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source va source_id bir biriga to'g'ri kelmadi")


# #shu source_id bo'yicha barcha fayllarni o'chirish
# def delete_source_files(source_id, db):
#     the_one(db, Categories, source_id)
#     source_files = db.query(Uploaded_files).filter(Uploaded_files.id == source_id).all()
#     for file in source_files:
#         delete_file(file.id, db)
#     db.commit()


