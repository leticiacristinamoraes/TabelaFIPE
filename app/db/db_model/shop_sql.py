from typing import List
import uuid
from sqlalchemy import UUID, Column, String

from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_model.db_base_postgresql import Base

#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Shops no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/shop.py
class ShopDBModel(Base):
    __tablename__ = 'Shops'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[String] = mapped_column(String)
    address:Mapped[String] = mapped_column(String)
    cnpj:Mapped[String] = mapped_column(String)
    registers: Mapped[List['RegisterDBModel']] = relationship(back_populates='shops')
    users_shops: Mapped[List['UserShopDBModel']] = relationship(back_populates='shops')