from db import Base
from sqlalchemy import Column, Integer, String


class Phones(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
