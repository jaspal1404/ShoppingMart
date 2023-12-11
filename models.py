from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    brand = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    delivery_method = Column(String)
    store_id = Column(Integer)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)



class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    brand = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    delivery_channel = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
