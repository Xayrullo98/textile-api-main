from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, func


class Supplier_balance(Base):
    __tablename__ = 'supplier_balance'
    id = Column(Integer, primary_key=True)
    balance = Column(Integer, nullable=False)
    currencies_id = Column(Integer,ForeignKey("currencies.id"), nullable=False)
    supplies_id = Column(Integer,ForeignKey("supplies.id"), nullable=False)
    user_id = Column(Integer, nullable=False)

    currency = relationship("Currencies",back_populates='balances')
    supply = relationship("Supplies",back_populates='balances')