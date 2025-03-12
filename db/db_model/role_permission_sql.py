from typing import List
import uuid
from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship


from db.db_model.db_base_postgresql import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

class RolePermissionDBModel(Base):
    __tablename__ = 'Roles_permissions'
    id: Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Roles.id'))
    permission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Permissions.id'))
    
    roles: Mapped[List['RoleDBModel']] = relationship(back_populates='roles_permissions')
    permissions: Mapped[List['PermissionDBModel']] = relationship(back_populates='roles_permissions')