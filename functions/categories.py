from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Categories.name.like(search_formatted) | Categories.comment.like(search_formatted)
    else:
        search_filter = Categories.id > 0

    categories = db.query(Categories).options(
        joinedload(Categories.stage)).filter(search_filter).order_by(Categories.id.desc())
    if page and limit:
        return pagination(categories, page, limit)
    else:
        return categories.all()


def one_category(id, db):
    return db.query(Categories).options(
        joinedload(Categories.order)).filter(Categories.id == id).first()


def create_category(form, db, thisuser):
    new_currencie_db = Categories(
        name=form.name,
        comment=form.comment,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)
    return new_currencie_db


def update_category(form, db, thisuser):
    the_one(db, Categories, form.id, thisuser)
    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.comment: form.comment,
        Categories.user_id: thisuser.id
    })
    db.commit()
