from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, and_, Numeric

from models.currencies import Currencies


class Supplier_balance(Base):
    __tablename__ = 'supplier_balance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Numeric, nullable=False)
    currencies_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)

    currency = relationship("Currencies", foreign_keys=[currencies_id],
                        primaryjoin=lambda: and_(Currencies.id == Supplier_balance.currencies_id))
