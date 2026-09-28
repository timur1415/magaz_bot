from sqlalchemy import Column, Integer, Uuid

from db.base import Base


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    anonymous_id = Column(Uuid, nullable=True)