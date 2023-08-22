from pydantic import BaseModel
from typing import Optional

class MeasureBase(BaseModel):
    name: str    


class MeasureCreate(MeasureBase):
    pass


class MeasureUpdate(MeasureBase):
    id: int
    status: bool

