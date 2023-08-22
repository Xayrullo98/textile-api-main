from pydantic import BaseModel, Field


class CreateOrder_history(BaseModel):
    order_id: int
    stage_id: int
    kpi_money: float = Field(..., ge=0)


class UpdateOrder_history(BaseModel):
    id: int
    order_id: int
    stage_id: int
    kpi_money: float = Field(..., ge=0)

