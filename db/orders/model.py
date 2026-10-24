from sqlalchemy import Column, Integer, String, Uuid

from db.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    anonymous_id = Column(Uuid, nullable=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)