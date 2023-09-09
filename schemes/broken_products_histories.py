from pydantic import BaseModel, Field


class CreateBroken_product_history(BaseModel):
    category_id: int
    done_product_quantity: float = Field(..., ge=0)
    brak_product_quantity: float = Field(..., ge=0)
    order_id: int


class UpdateBroken_product_history(BaseModel):
    id: int
    category_id: int
    done_product_quantity: float = Field(..., ge=0)
    brak_product_quantity: float = Field(..., ge=0)
    order_id: int