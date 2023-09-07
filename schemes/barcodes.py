from pydantic import BaseModel


class CreateBarcodes(BaseModel):
    name: str
    order_id: int
    stage_id: int


class UpdateBarcodes(BaseModel):
    id: int
    name: str
    order_id: int
    stage_id: int



