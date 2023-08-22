from pydantic import BaseModel, Field
from typing import Optional


class CurrenciesBase(BaseModel):
    name: str    
    money: float = Field(..., ge=0)


class CurrenciesCreate(CurrenciesBase):
    pass


class CurrenciesUpdate(CurrenciesBase):
    id: int
    status: bool

