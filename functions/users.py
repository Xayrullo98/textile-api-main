from sqlalchemy.orm import joinedload

from routes.login import get_password_hash
from utils.db_operations import save_in_db, the_one, the_one_username
from utils.pagination import pagination
from models.users import Users


def all_users(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Users.name.like(search_formatted) | Users.address.like(
            search_formatted) | Users.comment.like(search_formatted)
    else:
        search_filter = Users.id > 0

    users = db.query(Users).filter(search_filter).order_by(
        Users.id.desc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def create_user(form, db, thisuser):
    the_one_username(db=db, model=Users, username=form.username, thisuser=thisuser)
    new_user_db = Users(
        name=form.name,
        username=form.username,
        salary=form.salary,
        kpi=form.kpi,
        role=form.role,
        password_hash=get_password_hash(form.password_hash))
    save_in_db(db, new_us222er_db)


def one_user(id, db):
    return db.query(Users).options(
        joinedload(Users.order)).filter(Users.id == id).first()


def update_user(form, db, thisuser):
    the_one(db, Users, form.id, thisuser)
    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.password_hash: get_password_hash(form.password_hash),
        Users.salary: form.salary,
        Users.kpi: form.kpi,
        Users.status: form.status,
        Users.role: form.role,

    })
    db.commit()
