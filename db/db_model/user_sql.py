from typing import List
import uuid
from sqlalchemy import String

from db.db_model.db_base_postgresql import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Users no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/user.py
class UserDBModel(Base):
    __tablename__ = 'Users'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[String] = mapped_column(String)
    email: Mapped[String] = mapped_column(String)

    users_roles:Mapped[List['UserRoleDBModel']]  = relationship(back_populates='users')
    users_shops: Mapped[List['UserShopDBModel']] = relationship(back_populates='users')
