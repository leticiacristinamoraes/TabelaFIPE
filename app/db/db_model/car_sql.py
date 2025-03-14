from typing import List
import uuid
from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_model.db_base_postgresql import Base

#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Cars no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/car.py
class CarDBModel(Base):
    __tablename__ = 'Cars'

    id:Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand: Mapped[String] = mapped_column(String)
    model: Mapped[String] = mapped_column(String)
    model_year: Mapped[String] = mapped_column(String)

    avg_price: Mapped['AvgPriceDBModel'] = relationship(back_populates='car')
    registers: Mapped[List['RegisterDBModel']] = relationship(back_populates='cars')
    