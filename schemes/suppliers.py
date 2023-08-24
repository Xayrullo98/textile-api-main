from pydantic import BaseModel
from typing import Optional, List

from schemes.phones import CreatePhone


class SuppliersBase(BaseModel):
    name: str
    address: str
    comment: Optional[str]=''
    phones: List[CreatePhone]


class SuppliersCreate(SuppliersBase):
    pass


class SuppliersUpdate(SuppliersBase):
    id: int
    status: bool

