from datetime import date

from pydantic import BaseModel, Field


class CreateOrder(BaseModel):
    client_id: int
    category_id: int
    currency_id: int
    price: float = Field(..., ge=0)
    quantity: float = Field(..., ge=0)
    delivery_date: date
    status: int = Field(..., ge=0)
    order_status: bool


class UpdateOrder(BaseModel):
    id: int
    client_id: int
    category_id: int
    currency_id: int
    price: float = Field(..., ge=0)
    quantity: float = Field(..., ge=0)
    delivery_date: date
    status: int = Field(..., ge=0)
    order_status: bool