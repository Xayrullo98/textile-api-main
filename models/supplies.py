from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, DateTime, Numeric, Boolean,ForeignKey


class Supplies(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True)
    detail_id = Column(Integer, nullable=False)
    quantity = Column(Numeric, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    supplier_id = Column(Integer,ForeignKey("suppliers.id"), nullable=False)
    currency_id = Column(Integer,ForeignKey("currencies.id"), nullable=True)
    status = Column(Boolean, nullable=True,default=True)
    received_user_id = Column(Integer, nullable=True)

    supplier = relationship("Suppliers",back_populates='supply')
    currency = relationship("Currencies",back_populates='supply')
    balances = relationship("Supplier_balance", back_populates='supply')