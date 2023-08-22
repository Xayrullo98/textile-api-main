from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, func


class Measures(Base):
    __tablename__ = 'measures'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=False)

    category_detail = relationship("Category_details", back_populates='measure')
    stage = relationship("Stages", back_populates='measure')