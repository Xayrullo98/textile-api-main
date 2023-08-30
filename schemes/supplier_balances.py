from pydantic import BaseModel


class Supplier_balanceBase(BaseModel):
    balance: int
    currencies_id: int
    supplies_id: int


