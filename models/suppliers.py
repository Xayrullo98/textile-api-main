from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer


class Suppliers(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)


    supply = relationship("Supplies", back_populates='supplier')