from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Car(Base):
    __tablename__ = 'cars'
    id = Column(String, primary_key=True)
    brand = Column(String)
    model = Column(String)
    model_year = Column(String)
