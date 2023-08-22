from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.categories import Categories


class Broken_products(Base):
    __tablename__ = 'broken_products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    category_id = Column(Integer, nullable=False)
    quantity = Column(Numeric, nullable=False)

    category = relationship("Categories", foreign_keys=[category_id],
                            primaryjoin=lambda: and_(Categories.id == Broken_products.category_id))

