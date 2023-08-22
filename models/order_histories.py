from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.orders import Orders
from models.stages import Stages
from models.users import Users


class Order_histories(Base):
    __tablename__ = 'order_histories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer, nullable=False)
    date = Column(Date)
    stage_id = Column(Integer)
    user_id = Column(Integer)
    kpi_money = Column(Numeric)

    order = relationship("Orders", foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Order_histories.order_id))
    stage = relationship("Stages", foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Order_histories.stage_id))
    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Order_histories.user_id))