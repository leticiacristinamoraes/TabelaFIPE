from typing import List
import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db.db_model.db_base_postgresql import Base

#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Users_shops no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/user_shop.py
class UserShopDBModel(Base):
    __tablename__ = 'Users_shops'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Users.id'))
    shop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Shops.id'))

    users: Mapped[List['UserDBModel']]  = relationship(back_populates='users_shops')
    shops: Mapped[List['ShopDBModel']]  = relationship(back_populates='users_shops')