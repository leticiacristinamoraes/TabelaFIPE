import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from db.db_model.db_base_postgresql import Base

class RolePermissionDBModel(Base):
    __tablename__ = 'Roles_permissions'
    id = Column(uuid.UUID, primary_key=True)
    role_id = Column(uuid.UUID, ForeignKey('Permissions.id'))
    permission_id = Column(uuid.UUID, ForeignKey('Roles.id'))
    role = relationship("Role")
    permission = relationship("Permission")
    