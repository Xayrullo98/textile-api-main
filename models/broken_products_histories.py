from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.categories import Categories
from models.orders import Orders


class Broken_product_histories(Base):
    __tablename__ = 'broken_product_histories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    category_id = Column(Integer, nullable=False)
    done_product_quantity = Column(Numeric, nullable=False)
    brak_product_quantity = Column(Numeric, nullable=False)
    order_id = Column(Integer, nullable=False)

    category = relationship("Categories", foreign_keys=[category_id],
                            primaryjoin=lambda: and_(Categories.id == Broken_product_histories.category_id))
    order = relationship("Orders", foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Broken_product_histories.order_id))
