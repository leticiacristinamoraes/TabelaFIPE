from typing import List
import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, INT
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_model.db_base_postgresql import Base

#Essa classe é um objeto de mapeamento relacional (ORM) que representa a tabela Cars no Banco de Dados.
#Por ser um objeto de mapeamento relacional, ela é diferente da classe objeto do Python.
#Para usar a classe objeto do Python utilize a classe no app/entitites/car.py




class CarDBModel(Base):
    __tablename__ = 'Cars'

    id:Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[uuid.UUID] =  mapped_column(ForeignKey('Models.id'))
    model_year: Mapped[int] = mapped_column(INT)
    avg_price: Mapped['AvgPriceDBModel'] = relationship(back_populates='car')
    registers: Mapped[List['RegisterDBModel']] = relationship(back_populates='cars')
    models:  Mapped[List['ModelsDBModel']] = relationship(back_populates='car')