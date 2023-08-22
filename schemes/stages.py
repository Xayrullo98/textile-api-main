from pydantic import BaseModel


class CreateStage(BaseModel):
    name: str
    number: int
    comment: str
    status: bool
    kpi: float
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

