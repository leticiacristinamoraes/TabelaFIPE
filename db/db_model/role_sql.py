from typing import List
import uuid
from sqlalchemy import Column, String
from db.db_model.db_base_postgresql import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Roles no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/role.py
class RoleDBModel(Base):
    __tablename__ = 'Roles'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[String] = mapped_column(String)

    users_roles:Mapped[List['UserRoleDBModel']]  = relationship(back_populates='roles')
    roles_permissions: Mapped[List['RolePermissionDBModel']] = relationship(back_populates='roles')