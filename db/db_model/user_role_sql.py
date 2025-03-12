from typing import List
import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db.db_model.role_sql import RoleDBModel
from db.db_model.user_sql import UserDBModel
from db.db_model.db_base_postgresql import Base

class UserRoleDBModel(Base):
    __tablename__ = 'Users_roles'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Users.id'))
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Roles.id'))

    users: Mapped[List[UserDBModel]]  = relationship(back_populates='users_roles')
    roles: Mapped[List[RoleDBModel]]  = relationship(back_populates='users_roles')