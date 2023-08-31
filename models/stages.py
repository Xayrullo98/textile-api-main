from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Float


class Stages(Base):
    __tablename__ = 'stages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(565), nullable=False)
    number = Column(Integer, nullable=False, default=0)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    kpi = Column(Float, nullable=False)
    measure_id = Column(Integer, ForeignKey("measures.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    measure = relationship("Measures", back_populates='stage')
    category = relationship("Categories", back_populates='stage')
    stage_user = relationship("Stage_users", back_populates='stage')
    order_done_product = relationship("Order_done_products", back_populates='stage')
    order_for_master = relationship("Order_for_masters", back_populates='stage')
