from db import Base
from sqlalchemy import Column, String, Integer, Boolean


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False,default=True)
    name = Column(String(255), nullable=False)
    salary = Column(Integer, nullable=False)
    kpi = Column(Integer, nullable=False)
    role = Column(String(255), nullable=False)
    token = Column(String(255), nullable=True)