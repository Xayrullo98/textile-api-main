from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, update_phone, delete_phone
from models.phones import Phones
from routes.login import get_password_hash
from utils.db_operations import save_in_db, the_one, the_one_username
from utils.pagination import pagination
from models.users import Users


def all_users(search, page, limit, status, db):
    users = db.query(Users).options(joinedload(Users.user_phones))
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.name.like(search_formatted) | Users.username.like(search_formatted))
    else:
        users = users.filter(Users.id > 0)
    if status:
        users = users.filter(Users.status == True)
    elif status is False:
        users = users.filter(Users.status == False)
    else:
        users = users
    users = users.order_by(Users.id.desc())
    return pagination(users, page, limit)


def create_user(form, db, thisuser):
    the_one_username(db=db, model=Users, username=form.username)
    if form.role not in ['admin', 'stage_admin', 'stage_user', 'warehouseman']:
        raise HTTPException(status_code=400, detail="Role error")
    new_user_db = Users(
        name=form.name,
        username=form.username,
        salary=form.salary,
        balance=form.balance,
        role=form.role,
        password_hash=get_password_hash(form.password_hash))
    db.add(new_user_db)
    db.flush()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number=number, source='user', source_id=new_user_db.id, comment=comment, user_id=thisuser.id,
                     db=db, commit=False)
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_user(db, id):
    the_item = db.query(Users).options(
        joinedload(Users.user_phones)).filter(Users.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday user mavjud emas")


def update_user(form, thisuser, db):
    user = the_one(db=db, model=Users, id=form.id)
    if form.role not in ['admin', 'stage_admin', 'stage_user', 'warehouseman']:
        raise HTTPException(status_code=400, detail="Role error")
    if db.query(Users).filter(Users.username == form.username).first() and user.username != form.username:
        raise HTTPException(status_code=400, detail="Bu username bazada mavjud")
    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.password_hash: get_password_hash(form.password_hash),
        Users.salary: form.salary,
        Users.status: form.status,
        Users.role: form.role,

    })

    user_phones = db.query(Phones).filter(Phones.source_id == user.id).all()
    for phone in user_phones:
        delete_phone(id=phone.id, db=db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number=number, source='user', source_id=user.id, comment=comment, user_id=thisuser.id,
                     db=db, commit=False)
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def add_user_balance(user_id, money, db):
    user = db.query(Users).filter(Users.id == user_id).first()
    user_balance = user.balance + money
    db.query(Users).filter(Users.id == user_id).update({
        Users.balance: user_balance
    })
    db.commit()

def sup_user_balance(user_id, money, db):
    user = db.query(Users).filter(Users.id == user_id).first()
    user_balance = user.balance - money
    db.query(Users).filter(Users.id == user_id).update({
        Users.balance: user_balance
    })
    db.commit()