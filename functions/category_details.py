from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.measures import Measures
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.category_details import Category_details


def all_category_details(search, measure_id, category_id, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Category_details.name.like(search_formatted) | Category_details.quantity.like(search_formatted)
    else:
        search_filter = Category_details.id > 0
    if measure_id:
        search_measure_id = Category_details.measure_id == measure_id
    else:
        search_measure_id = Category_details.measure_id > 0

    if category_id:
        search_category_id = Category_details.category_id == category_id
    else:
        search_category_id = Category_details.category_id > 0

    category_details = db.query(Category_details).options(
        joinedload(Category_details.category, Category_details.measure, )).filter(search_filter, search_measure_id,
                                                                                  search_category_id).order_by(
        Category_details.id.desc())
    if page and limit:
        return pagination(category_details, page, limit)
    else:
        return category_details.all()


def one_category_detail(id, db):
    return db.query(Category_details).options(
        joinedload(Category_details.category, Category_details.measure, )).filter(Categories.id == id).first()


def create_category_detail(form, db, thisuser):
    the_one_model_name(model=Category_details, name=form.name, db=db)
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
    new_currencie_db = Category_details(
        name=form.name,
        quantity=form.quantity,
        measure_id=form.measure_id,
        category_id=form.category_id,
        comment=form.comment,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)
    return new_currencie_db


def update_category_detail(form, db, thisuser):
    the_one(db, Category_details, form.id)
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
    db.query(Category_details).filter(Category_details.id == form.id).update({
        Category_details.name: form.name,
        Category_details.quantity: form.quantity,
        Category_details.measure_id: form.measure_id,
        Category_details.category_id: form.category_id,
        Category_details.comment: form.comment,
        Category_details.user_id: thisuser.id
    })
    db.commit()
