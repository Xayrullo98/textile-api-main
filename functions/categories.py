from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search, status, page, limit, db):
    categories_query = db.query(Categories)

    if search:
        search_formatted = f"%{search}%"
        search_filter = Categories.name.ilike(search_formatted) | Categories.comment.ilike(search_formatted)
        categories_query = categories_query.filter(search_filter)
    else:
        categories_query = categories_query.filter(Categories.id > 0)

    if status:
        categories_query = categories_query.filter(Categories.status == True)
    elif status is False:
        categories_query = categories_query.filter(Categories.status == False)
    else:
        categories = categories_query
    categories_query = categories_query.order_by(Categories.id.desc())

    return pagination(categories_query, page, limit)


def create_category(form, db, thisuser):
    the_one_model_name(db, Categories, form.name)
    new_currencie_db = Categories(
        name=form.name,
        comment=form.comment,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)
    return new_currencie_db


def update_category(form, thisuser, db):
    category = the_one(db, Categories, form.id)
    if db.query(Categories).filter(Categories.name == form.name).first() and category.name != form.name:
        raise HTTPException(status_code=400, detail=f"Bazada bunday name({form.name}) mavjud!")
    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.comment: form.comment,
        Categories.user_id: thisuser.id
    })
    db.commit()
