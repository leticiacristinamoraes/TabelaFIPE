from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class CarDBModel(Base):
    __tablename__ = 'permissions'
    id = Column(String, primary_key=True)
    name = Column(String)