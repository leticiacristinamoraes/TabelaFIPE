import uuid
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
class RolePermissionDBModel(Base):
    __tablename__ = 'Roles_permissions'
    id = Column(uuid.UUID, primary_key=True)
    role_id = Column(uuid.UUID, ForeignKey('Permissions.id'))
    permission_id = Column(uuid.UUID, ForeignKey('Roles.id'))
    role = relationship("Role")
    permission = relationship("Permission")
    