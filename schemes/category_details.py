from pydantic import BaseModel
from typing import Optional

class Category_detailsBase(BaseModel):
    name: str
    quantity: float = 0
    measure_id:int
    category_id:int
    comment:Optional[str]=''


class Category_detailsCreate(Category_detailsBase):
    pass


class Category_detailsUpdate(Category_detailsBase):
    id: int
    status: bool

