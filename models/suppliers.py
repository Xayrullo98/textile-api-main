from db import Base
from sqlalchemy import Column, String, Integer, DateTime


class Suppliers(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    balance = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
