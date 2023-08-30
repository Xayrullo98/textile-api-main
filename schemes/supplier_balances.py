from pydantic import BaseModel
from typing import Optional

class Supplier_balanceBase(BaseModel):
    balance: int
    currencies_id:int
    supplies_id:int


class Supplier_balanceCreate(Supplier_balanceBase):
    pass


class Supplier_balanceUpdate(Supplier_balanceBase):
    id: int
    status: bool

