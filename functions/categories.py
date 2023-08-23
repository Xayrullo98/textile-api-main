from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search, status, page, limit, db):
    categories = db.query(Categories)
    if search:
        search_formatted = "%{}%".format(search)
        categories = categories.name.like(search_formatted) | Categories.comment.like(search_formatted)
    else:
        categories = Categories.id > 0
    if status:
        categories = categories.filter(Categories.status == True)
    elif status is False:
        categories = categories.filter(Categories.status == False)
    else:
        categories = categories
    categories = categories.order_by(Categories.id.desc())

    return pagination(categories, page, limit)


def create_category(form, db, thisuser):
    the_one_model_name(db, Categories, form.name)
    new_currencie_db = Categories(
        name=form.name,
        comment=form.comment,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)
    return new_currencie_db


def update_category(form, db, thisuser):
    the_one(db, Categories, form.id)
    the_one_model_name(db, Categories, form.name)
    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.comment: form.comment,
        Categories.user_id: thisuser.id
    })
    db.commit()
