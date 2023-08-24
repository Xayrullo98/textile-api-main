from pydantic import BaseModel, Field


class CreatePhone(BaseModel):
    number: str = Field(..., min_length=9, max_length=9)
    comment: str


class UpdatePhone(BaseModel):
    id: int
    number: str = Field(..., min_length=9, max_length=9)
    comment: str
