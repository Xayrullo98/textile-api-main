from pydantic import BaseModel, Field


class CreateOrder_done_products(BaseModel):
    order_id: int
    stage_id: int
    quantity: float = Field(..., ge=0)


class UpdateOrder_done_products(BaseModel):
    id: int
    order_id: int
    stage_id: int
    worker_id: int
    quantity: float = Field(..., ge=0)

