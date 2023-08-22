from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, func


class Currencies(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    money = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    balances = relationship("Supplier_balance", back_populates='currency')
    supply = relationship("Supplies", back_populates='currency')