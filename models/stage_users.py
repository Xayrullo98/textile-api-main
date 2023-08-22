from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer,ForeignKey



class Stage_users(Base):
    __tablename__ = 'stage_users'
    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer,ForeignKey("Stages.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    crated_user_id = Column(Integer,ForeignKey("Users.id"), nullable=False)

    stage = relationship("Stages", back_populates='stage_user')
    connected_user = relationship("Users", back_populates='stage_user')




