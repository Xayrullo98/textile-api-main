from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, DateTime, Numeric, Boolean, ForeignKey, and_

from models.users import Users


class Supplies(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_detail_id = Column(Integer, ForeignKey("category_details.id"), nullable=False)
    quantity = Column(Numeric, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)
    status = Column(Boolean, nullable=True, default=False)
    received_user_id = Column(Integer, nullable=True)

    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.user_id))
    received_user = relationship("Users", foreign_keys=[received_user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.received_user_id))
    supplier = relationship("Suppliers", back_populates='supply')
    currency = relationship("Currencies", back_populates='supply')
    category_detail = relationship('Category_details', back_populates='supply')