from typing import List
import uuid
from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship
from db.db_model.db_base_postgresql import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Roles_permissions no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/role_permission.py
class RolePermissionDBModel(Base):
    __tablename__ = 'Roles_permissions'
    id: Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Roles.id'))
    permission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Permissions.id'))
    
    roles: Mapped[List['RoleDBModel']] = relationship(back_populates='roles_permissions')
    permissions: Mapped[List['PermissionDBModel']] = relationship(back_populates='roles_permissions')