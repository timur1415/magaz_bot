from db.base import Base
from sqlalchemy import Column, Integer,String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String)
    password = Column(String)
    phone_number = Column(String)
    address = Column(String)
    