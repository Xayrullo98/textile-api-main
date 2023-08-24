from decimal import Decimal

from pydantic import BaseModel, Field


class CreateIncome(BaseModel):
    money: Decimal = Field(..., ge=0)
    currency_id: int
    source: str
    source_id: int
    comment: str
    kassa_id: int


class UpdateIncome(BaseModel):
    id: int
    money: Decimal = Field(..., ge=0)
    currency_id: int
    source: str
    source_id: int
    comment: str
    kassa_id: int

