from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
Base = declarative_base()

class Register(Base):
    __tablename__ = 'Registers'
    id = Column(String, primary_key=True)
    shop_id = Column(String, ForeignKey('Shops.id'))
    car_id = Column(String, ForeignKey('Cars.id'))
    created_date = Column(Date)
    price = Column(Float)
    shop = relationship("Shops")
    car = relationship("Cars")