from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
class RolePermission(Base):
    __tablename__ = 'Roles_permissions'
    id = Column(String, primary_key=True)
    role_id = Column(String, ForeignKey('Permission.id'))
    permission_id = Column(String, ForeignKey('Roles.id'))
    role = relationship("Roles")
    permission = relationship("Permission")
    