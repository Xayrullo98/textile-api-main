from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, and_, Numeric

from models.currencies import Currencies


class Supplier_balance(Base):
    __tablename__ = 'supplier_balance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Numeric, nullable=False) #0, #0
    currencies_id = Column(Integer, nullable=False) #1, 2
    supplier_id = Column(Integer, nullable=False) #1 #1

    currency = relationship("Currencies", foreign_keys=[currencies_id],
                        primaryjoin=lambda: and_(Currencies.id == Supplier_balance.currencies_id))
