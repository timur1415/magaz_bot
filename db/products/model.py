from db.base import Base
from sqlalchemy import Column, Integer,String

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price=Column(Integer)
    photo=Column(String)
    description=Column(String)


