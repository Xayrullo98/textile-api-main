from pydantic import BaseModel, Field


class CreateStage(BaseModel):
    name: str
    number: int
    comment: str
    status: bool
    kpi: float = Field(...,ge=0.1)
    measure_id: int
    category_id: int


class UpdateStage(BaseModel):
    id: int
    name: str
    number: int
    comment: str
    status: bool
    kpi: float
    measure_id: int
    category_id: int

