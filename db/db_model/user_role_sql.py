import uuid
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
class UserRoleDBModel(Base):
    __tablename__ = 'Users_roles'
    id = Column(uuid.UUID, primary_key=True)
    user_id = Column(uuid.UUID, ForeignKey('Users.id'))
    role_id = Column(uuid.UUID, ForeignKey('Roles.id'))
    user = relationship("User")
    role = relationship("Role")