from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, update_phone, delete_phone
from models.phones import Phones
from routes.login import get_password_hash
from utils.db_operations import save_in_db, the_one, the_one_username
from utils.pagination import pagination
from models.users import Users


def all_users(search, page, limit, status, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Users.name.like(search_formatted) | Users.address.like(
            search_formatted) | Users.comment.like(search_formatted)
    else:
        search_filter = Users.id > 0

    users = db.query(Users).filter(search_filter).options(joinedload(Users.phones)).order_by(
        Users.id.desc())
    if status:
        users = users.filter(Users.status==True)
    else:
        users = users.filter(Users.status==False)
        

    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def create_user(form, db, thisuser):
    the_one_username(db=db, model=Users, username=form.username)
    new_user_db = Users(
        name=form.name,
        username=form.username,
        salary=form.salary,
        kpi=form.kpi,
        role=form.role,
        password_hash=get_password_hash(form.password_hash))
    save_in_db(db, new_user_db)
    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
            raise HTTPException(status_code=400, detail="Bu nomer bazada mavjud")
        else:
            number = i.number
            create_phone(number=number, source='user', source_id=new_user_db.id, comment=comment, user_id=thisuser.id, db=db)
    raise HTTPException(status_code=200, detail=f"Amaliyot muvvaffaqqiyatli bajarildi")




def one_user( db, id):
    the_item = db.query(Users).options(
        joinedload(Users.phones)).filter(Users.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday user mavjud emas")


def update_user(form, thisuser, db):
    user = the_one(db=db, model=Users, id=form.id)
    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.password_hash: get_password_hash(form.password_hash),
        Users.salary: form.salary,
        Users.status: form.status,
        Users.role: form.role,

    })
    db.commit()
    user_phones = db.query(Phones).filter(Phones.source_id == user.id).all()
    for phone in user_phones:
        delete_phone(id=phone.id, db=db)

    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
            raise HTTPException(status_code=400, detail="Bu nomer bazada mavjud")
        else:
            number = i.number
            create_phone(number=number, source='user', source_id=user.id, comment=comment, user_id=thisuser.id,
                         db=db)
    raise HTTPException(status_code=200, detail=f"Amaliyot muvvaffaqqiyatli bajarildi")
