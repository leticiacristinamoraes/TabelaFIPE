import uuid
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class PermissionDBModel(Base):
    __tablename__ = 'permissions'
    id = Column(uuid.UUID, primary_key=True)
    name = Column(String)