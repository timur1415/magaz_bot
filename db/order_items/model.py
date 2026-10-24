from sqlalchemy import Column, Integer

from db.base import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=True)
    product_id = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)