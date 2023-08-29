from datetime import date, datetime

from fastapi import HTTPException
from sqlalchemy import func, String
from sqlalchemy.orm import joinedload

from functions.supplier_balances import create_supplier_balance_func
from functions.warehouse_products import create_warehouse_product
from models.category_details import Category_details
from models.currencies import Currencies
from models.supplier_balances import Supplier_balance
from models.suppliers import Suppliers
from models.users import Users
from models.warehouse_products import Warehouse_products
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.supplies import Supplies


def all_supplies(search, category_detail_id, supplier_id, currency_id, status, page, limit, db):
    supplies = db.query(Supplies).options(
        joinedload(Supplies.currency),
        joinedload(Supplies.category_detail),
        joinedload(Supplies.supplier),
        joinedload(Supplies.received_user),
        joinedload(Supplies.user)
    )

    if search:
        search_formatted = f"%{search}%"
        supplies = supplies.filter(Supplies.quantity.like(search_formatted) |
                                   Supplies.price.like(search_formatted))
    else:
        supplies = supplies.filter(Supplies.id > 0)

    #status bo'yicha filterlash
    if status:
        supplies = supplies.filter(Supplies.status == True)
    if status==False:
        supplies = supplies.filter(Supplies.status == False)
    if category_detail_id:
        supplies = supplies.filter(Supplies.category_detail_id == category_detail_id)
    if supplier_id:
        supplies = supplies.filter(Supplies.supplier_id == supplier_id)
    if currency_id:
        supplies = supplies.filter(Supplies.currency_id == currency_id)

    supplies = supplies.order_by(Supplies.id.desc())
    return pagination(supplies, page, limit)


def one_supply(id, db):
    the_item = db.query(Supplies).options(joinedload(Supplies.currency), joinedload(Supplies.category_detail),
                                          joinedload(Supplies.supplier), joinedload(Supplies.received_user),
                                          joinedload(Supplies.user)).filter(Supplies.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="bazada bunday ma'lumot yo'q")
    return the_item


def create_supply(form, thisuser, db):
    the_one(db=db, model=Suppliers, id=form.supplier_id)
    the_one(db=db, model=Currencies, id=form.currency_id)
    the_one(db, Category_details, form.category_detail_id)
    new_supplier_db = Supplies(
        category_detail_id=form.category_detail_id,
        quantity=form.quantity,
        price=form.price,
        supplier_id=form.supplier_id,
        date=datetime.now(),
        currency_id=form.currency_id,
        user_id=thisuser.id
    )
    save_in_db(db, new_supplier_db)
    # after created supply, it should be added warehouse_products



#agar supplyni stutusi true bo'lsa uni update qila olmaydi
def update_supply(form, thisuser, db):
    the_one(db=db, model=Suppliers, id=form.supplier_id)
    the_one(db=db, model=Currencies, id=form.currency_id)
    the_one(db, Category_details, form.category_detail_id)
    supply = the_one(db, Supplies, form.id)
    the_one(db, Users, form.received_user_id)
    if supply.status:
        raise HTTPException(status_code=400, detail="Bu supplayni statusi true o'zgartirib bo'lmaydi")
    supply_quantity = one_supply(id=form.id,db=db)
    differance = supply_quantity.quantity-form.quantity
    create_warehouse_product(category_detail_id=form.category_detail_id,quantity=differance,price=form.price,currency_id=form.currency_id,db=db,thisuser=thisuser)
    db.query(Supplies).filter(Supplies.id == form.id).update({
        Supplies.category_detail_id: form.category_detail_id,
        Supplies.quantity: form.quantity,
        Supplies.price: form.price,
        Supplies.date: datetime.now(),
        Supplies.supplier_id: form.supplier_id,
        Supplies.currency_id: form.currency_id,
        Supplies.user_id: thisuser.id
    })
    db.commit()

    balance = supply_quantity.quantity*supply_quantity.price
    differance_balance = balance-form.quantity*form.price
    supplier = db.query(Supplier_balance).filter(Supplier_balance.supplies_id==form.id).first()
    balance = supplier.balance+differance_balance
    db.query(Supplier_balance).filter(Supplier_balance.supplies_id == form.id).update({
        Supplier_balance.balance: balance,
        Supplier_balance.currencies_id: form.currency_id,
        Supplier_balance.user_id: thisuser.id,
    })
    db.commit()


def supply_confirm(id, thisuser,  db):
    supply = the_one(db, Supplies, id)
    print(supply.category_detail_id,'ssssssssssssssssssssssssssssssssssssssssssss')
    print(supply.price,'ssssssssssssssssssssssssssssssssssssssssssss')
    print(supply.quantity,'ssssssssssssssssssssssssssssssssssssssssssss')
    print(supply.currency_id,'ssssssssssssssssssssssssssssssssssssssssssss')
    # if thisuser.role != 'warehouseman':
    #     raise HTTPException(status_code=400, detail="Faqat omborchi taminotni qabul qilishi mumkin")
    create_warehouse_product(category_detail_id=supply.category_detail_id, quantity=supply.quantity,
                             price=supply.price, currency_id=supply.currency_id, db=db, thisuser=thisuser)

    create_supplier_balance_func(balance=supply.quantity * supply.price, currencies_id=supply.currency_id,
                                 supplies_id=supply.id, db=db, thisuser=thisuser)
    if supply.status == False:
        db.query(Supplies).filter(Supplies.id == id).update({
            Supplies.status: True,
            Supplies.received_user_id: thisuser.id
        })
        db.commit()
        return {"data":"Tasdiqlandi"}
    else:
        raise HTTPException(status_code=400, detail="Bu supply allaqochan tasdiqlangan!")


#agar supplyni stutusi true bo'lsa uni o'chira olmaydi
def delete_supply(id, db, thisuser):
    supply = the_one(db=db, model=Supplies, id=id)
    if supply.status:
        raise HTTPException(status_code=400, detail="Bu supplayni statusi true o'chira olmaysiz")
    db.query(Supplies).filter(Supplies.id == id).delete()
    db.commit()

