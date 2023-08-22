from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db import Base,database


def get_in_db(
        db: Session,
        model,
        ident: int
):
    obj = db.query(model).get(ident)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bazada bunday {model} yoq"
        )
    return obj


def save_in_db(
        db: database,
        obj: Base
):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def the_one(db, model, id, thisuser):
    the_one = db.query(model).filter(model.id == id,).first()
    if not the_one:
        raise HTTPException(status_code=400, detail=f"Bazada bunday {model} yo'q!")
    return the_one


def the_one_username(db, model, username, thisuser):
    the_one = db.query(model).filter(model.username == username,).first()
    if  the_one:
        raise HTTPException(status_code=400, detail=f"Bazada bunday username({username}) mavjud!")
    return the_one