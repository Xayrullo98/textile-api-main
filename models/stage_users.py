from db import Base
from sqlalchemy import Column, Integer


class Stage_users(Base):
    __tablename__ = 'stage_users'
    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    crated_user_id = Column(Integer, nullable=False)
