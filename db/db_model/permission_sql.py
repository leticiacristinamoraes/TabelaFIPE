from typing import List
import uuid
from sqlalchemy import Column, String
from db.db_model.db_base_postgresql import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

#Classe relacionada a tabela Permissions no Banco de Dados
class PermissionDBModel(Base):
    __tablename__ = 'Permissions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[String] = mapped_column(String)

    roles_permissions:Mapped[List['RolePermissionDBModel']] = relationship(back_populates='permissions')