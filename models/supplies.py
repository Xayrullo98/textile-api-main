from db import Base
from sqlalchemy import Column, String, Integer, DateTime, Numeric


class Supplies(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    measure = Column(String(255), nullable=False)
    price = Column(Numeric, nullable=False)
    date = Column(DateTime, nullable=False)
    quantity = Column(Numeric, nullable=False)
    user_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    received_quantity = Column(Numeric, nullable=True)
    received_date = Column(DateTime, nullable=True)
    received_user_id = Column(Integer, nullable=True)
