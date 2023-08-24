from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, ForeignKey, Float


class Order_done_products(Base):
    __tablename__ = 'order_done_products'
    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Float, nullable=False)

    stage = relationship("Stages", back_populates='order_done_product')
    order = relationship("Orders", back_populates='order_done_product')
    user = relationship("Users", back_populates='order_done_product')
