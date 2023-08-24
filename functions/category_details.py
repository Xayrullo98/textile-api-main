from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.measures import Measures
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.category_details import Category_details


def all_category_details(search, measure_id, category_id, page, limit, db):
    category_details = db.query(Category_details).options(
        joinedload(Category_details.category),
        joinedload(Category_details.measure))
    if search:
        search_formatted = "%{}%".format(search)
        category_details = category_details.name.like(search_formatted)
    else:
        category_details = category_details
    if measure_id:
        category_details = category_details.filter(Category_details.measure_id == measure_id)
    else:
        category_details = category_details

    if category_id:
        category_details = category_details.filter(Category_details.category_id == category_id)
    else:
        category_details = category_details

    category_details = category_details.order_by(Category_details.id.desc())

    return pagination(category_details, page, limit)


def one_category_detail(id, db):
    the_item = db.query(Category_details).options(
        joinedload(Category_details.category, Category_details.measure, )).filter(Categories.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bu malumot bazada mavjud")

def create_category_detail(form, db, thisuser):
    the_one_model_name(db, Category_details, form.name)
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


def update_category_detail(form, db, thisuser):
    category_detail = the_one(db, Category_details, form.id)
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
    if db.query(Category_details).filter(Category_details.name == form.name).first() and category_detail.name != form.name:
        raise HTTPException(status_code=400, detail=f"Bazada bunday number({form.number}) mavjud!")
    db.query(Category_details).filter(Category_details.id == form.id).update({
        Category_details.name: form.name,
        Category_details.quantity: form.quantity,
        Category_details.measure_id: form.measure_id,
        Category_details.category_id: form.category_id,
        Category_details.comment: form.comment,
        Category_details.user_id: thisuser.id
    })
    db.commit()
