from pydantic import BaseModel, Field


class CreateBroken_product(BaseModel):
    category_id: int
    quantity: float = Field(..., ge=0)


class UpdateBroken_product(BaseModel):
    id: int
    category_id: int
    quantity: float = Field(..., ge=0)