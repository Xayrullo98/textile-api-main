from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, Boolean,Float


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False,default=True)
    name = Column(String(255), nullable=False)
    salary = Column(Integer, nullable=False)
    balance = Column(Float, nullable=True,default=0)
    role = Column(String(255), nullable=False)
    token = Column(String(255), nullable=True)

    stage_user = relationship("Stage_users", back_populates='connected_user')
    order_done_product = relationship("Order_done_products", back_populates='user')
    order_for_master = relationship("Order_for_masters", back_populates='user')