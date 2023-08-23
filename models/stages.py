from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey


class Stages(Base):
    __tablename__ = 'stages'
    id = Column(Integer, primary_key=True)
    name = Column(String(565), nullable=False)
    number = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    kpi = Column(Numeric, nullable=False)
    measure_id = Column(Integer, ForeignKey("measures.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    measure = relationship("Measures", back_populates='stage')
    category = relationship("Categories", back_populates='stage')
    stage_user = relationship("Stage_users", back_populates='stage')
