from pydantic import BaseModel
from typing import Optional


class SuppliesBase(BaseModel):
    detail_id: int
    quantity: int
    price: int
    supplier_id: int
    currency_id: int


class SuppliesCreate(SuppliesBase):
    pass


class SuppliesUpdate(SuppliesBase):
    id: int
    received_user_id: int
    status: bool
