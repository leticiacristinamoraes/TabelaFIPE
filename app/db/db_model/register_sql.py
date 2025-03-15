import datetime
from typing import List
import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db.db_model.db_base_postgresql import Base

#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Registers no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/register.py
class RegisterDBModel(Base):
    __tablename__ = 'Registers'
    
    id: Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Shops.id'))
    car_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Cars.id'))
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    price: Mapped[float] = mapped_column(Numeric(10,2))

    shops: Mapped[List['ShopDBModel']] = relationship( back_populates='registers')
    cars: Mapped[List['CarDBModel']] = relationship(back_populates='registers')