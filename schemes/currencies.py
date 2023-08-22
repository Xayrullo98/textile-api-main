from pydantic import BaseModel
from typing import Optional

class CurrenciesBase(BaseModel):
    name: str    
    money:str


class CurrenciesCreate(CurrenciesBase):
    pass


class CurrenciesUpdate(CurrenciesBase):
    id: int
    status: bool

