from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, ForeignKey, Float,DateTime,func


class Order_for_masters(Base):
    __tablename__ = 'order_for_masters'
    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer,  nullable=False)
    connected_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    datetime = Column(DateTime,default=func.now(), nullable=False)

    stage = relationship("Stages", back_populates='order_for_master')
    order = relationship("Orders", back_populates='order_for_master')
    user = relationship("Users", back_populates='order_for_master')
