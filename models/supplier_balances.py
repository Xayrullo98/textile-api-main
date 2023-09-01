from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, ForeignKey


class Supplier_balance(Base):
    __tablename__ = 'supplier_balance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Integer, nullable=False)
    currencies_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    supplier_id = Column(Integer, nullable=False)

    currency = relationship("Currencies", back_populates='balances')
