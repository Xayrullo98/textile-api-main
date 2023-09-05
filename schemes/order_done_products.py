import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.datetime_parse import date

class CreateOrder_done_products(BaseModel):
    order_id: int
    worker_id: int
    stage_id: int
    quantity: float = Field(..., ge=0)




class UpdateOrder_done_products(BaseModel):
    id: int
    worker_id: int
    stage_id: int
    quantity: float = Field(..., ge=0)
    kpi_money: float = Field(..., ge=0)

