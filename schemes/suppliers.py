from pydantic import BaseModel
from typing import Optional


class SuppliersBase(BaseModel):
    name: str
    address: str
    comment: Optional[str]=''


class SuppliersCreate(SuppliersBase):
    pass


class SuppliersUpdate(SuppliersBase):
    id: int
    status: bool

