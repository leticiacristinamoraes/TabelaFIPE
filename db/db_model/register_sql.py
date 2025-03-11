import uuid
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
Base = declarative_base()

class RegisterDBModel(Base):
    __tablename__ = 'Registers'
    id = Column(uuid.UUID, primary_key=True)
    shop_id = Column(uuid.UUID, ForeignKey('Shops.id'))
    car_id = Column(uuid.UUID, ForeignKey('Cars.id'))
    created_date = Column(Date)
    price = Column(String)
    shop = relationship("Shop")
    car = relationship("Car")