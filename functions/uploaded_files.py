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
                                          joinedload(Uploaded_files.category).load_only(Categories.name))
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


def create_file(new_file, source, source_id, comment, thisuser, db):
    if source not in ['category']:
        raise HTTPException(status_code=400, detail="Source error")
    the_one(db, Categories, source_id)
    if db.query(Uploaded_files).filter(Uploaded_files.source == source,
                                       Uploaded_files.source_id == source_id).first():
        raise HTTPException(status_code=400, detail="This source already have his own file!")
    if db.query(Categories).filter(Categories.id == source_id).first() and source == "category":
        file_location = new_file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"Uploaded_files/{new_file.filename}", "wb+") as file_object:
            file_object.write(new_file.file.read())
        new_file_db = Uploaded_files(
            file=new_file.filename,
            source=source,
            source_id=source_id,
            comment=comment,
            user_id=thisuser.id,
        )
        save_in_db(db, new_file_db)
    else:
        raise HTTPException(status_code=400, detail="source va source_id bir-biriga mos kelmadi!")


def update_file(id, new_file, source, source_id, comment, this_user, db):
    the_one(db, Uploaded_files, id)
    if source not in ['category']:
        raise HTTPException(status_code=400, detail="Source error")
    the_one(db, Categories, source_id)
    this_file = db.query(Uploaded_files).filter(Uploaded_files.source == source,
                                                Uploaded_files.source_id == source_id).first()
    if this_file and this_file.id != id:
        raise HTTPException(status_code=400,
                            detail="Siz kiritayotgan idli file ushbu sourcega tegishli "
                                   "emas va siz kiritayotgan sourcening ozini fayli bor")
    if db.query(Categories).filter(Categories.id == source_id).first() and source == "category":

        file_location = new_file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"Uploaded_files/{file_location}", "wb+") as file_object:
            file_object.write(new_file.file.read())
        db.query(Uploaded_files).filter(Uploaded_files.id == id).update({
            Uploaded_files.file: new_file.filename,
            Uploaded_files.source: source,
            Uploaded_files.source_id: source_id,
            Uploaded_files.comment: comment,
            Uploaded_files.user_id: this_user.id
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source va source_id bir-biriga mos kelmadi!")


# def delete_file(id, db):
#     the_one(id, Uploaded, db)
#     db.query(Uploaded).filter(Uploaded.id == id).delete()
#     db.commit()
