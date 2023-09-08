from db import Base
from sqlalchemy import Column, Integer, String, Boolean


class Barcodes(Base):
    __tablename__ = 'barcodes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    order_id = Column(Integer, nullable=False)
    stage_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False,default=True)
    user_id = Column(Integer, nullable=False)