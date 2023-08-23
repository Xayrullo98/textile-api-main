from typing import List

from pydantic import BaseModel, Field

from schemes.phones import CreatePhone, UpdatePhone


class CreateKassa(BaseModel):
    name: str
    comment: str
    currency_id: int
    phones: List[CreatePhone]


class UpdateKassa(BaseModel):
    id: int
    name: str
    comment: str
    phones: List[UpdatePhone]

