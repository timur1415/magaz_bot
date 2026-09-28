from db.base import Base
from sqlalchemy import Column, Integer,String

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, nullable=True)
    product_id = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)