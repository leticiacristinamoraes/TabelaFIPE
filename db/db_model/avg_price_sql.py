from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
class AvgPriceDBModel(Base):
    __tablename__ = 'Avg_price'
    id = Column(String, primary_key=True)
    car_id = Column(String, ForeignKey('Cars.id'))
    avg_price = Column(String)
    car = relationship("Cars")
    