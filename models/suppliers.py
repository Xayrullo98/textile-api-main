from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, and_

from models.users import Users
from models.supplier_balances import Supplier_balance


class Suppliers(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)

    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Suppliers.user_id))

    balances = relationship("Supplier_balance", foreign_keys=[id],
                        primaryjoin=lambda: and_(Supplier_balance.supplier_id == Suppliers.id))

