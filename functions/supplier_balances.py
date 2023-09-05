from utils.db_operations import save_in_db
from models.supplier_balances import Supplier_balance


def create_supplier_balance_func(balance, currencies_id, supplier_id, db):
    new_supplier_balance_db = Supplier_balance(
        balance=balance,
        currencies_id=currencies_id,
        supplier_id=supplier_id,
    )
    save_in_db(db, new_supplier_balance_db)


def expense_supplier_balance(money, currency_id, supplier_id, db):
    """Xarajat qilinganda supplier_balansidan ayiramiz"""

    db.query(Supplier_balance).filter(Supplier_balance.supplier_id == supplier_id,
                                      Supplier_balance.currencies_id == currency_id).update({
        Supplier_balance.balance: Supplier_balance.balance - money
    })
    db.commit()



