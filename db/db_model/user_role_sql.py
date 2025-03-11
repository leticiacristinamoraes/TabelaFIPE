from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
class UserRole(Base):
    __tablename__ = 'Users_roles'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('Users.id'))
    role_id = Column(String, ForeignKey('Roles.id'))
    user = relationship("Users")
    role = relationship("Roles")