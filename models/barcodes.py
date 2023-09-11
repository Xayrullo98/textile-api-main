from db import Base
from sqlalchemy import Column, Integer


class Barcodes(Base):
    __tablename__ = 'barcodes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer, nullable=False)
    stage_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)