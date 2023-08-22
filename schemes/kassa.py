from pydantic import BaseModel, Field


class CreateKassa(BaseModel):
    name: str
    comment: str
    currency_id: int


class UpdateKassa(BaseModel):
    id: int
    name: str
    comment: str
    currency_id: int
