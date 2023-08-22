from typing import List
from pydantic import BaseModel
from schemes.phones import CreatePhone


class CreateUser(BaseModel):
    name: str
    username: str
    password_hash: str
    role: str
    kpi: float
    status: bool
    salary: float
    phones: List[CreatePhone]


class UpdateUser(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    salary: float
    phones: List[CreatePhone]


class TokenUser(BaseModel):
    id: int
    username: str
    role: str
    token: str


class UserCurrent(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool

