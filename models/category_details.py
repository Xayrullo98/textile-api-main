from db import Base
from sqlalchemy import Column, String, Integer, and_, ForeignKey
from sqlalchemy.orm import relationship

from models.users import Users


class Category_details(Base):
    __tablename__ = 'category_details'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    measure_id = Column(Integer, ForeignKey('measures.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Category_details.user_id))

    measure = relationship('Measures', back_populates='category_detail')
    category = relationship('Categories', back_populates='category_detail')
    supply = relationship('Supplies', back_populates='category_detail')

