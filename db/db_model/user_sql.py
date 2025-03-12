from typing import List
import uuid
from sqlalchemy import String

from db.db_model.db_base_postgresql import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class UserDBModel(Base):
    __tablename__ = 'Users'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[String] = mapped_column(String)
    email: Mapped[String] = mapped_column(String)

    users_roles:Mapped[List['UserRoleDBModel']]  = relationship(back_populates='users')

