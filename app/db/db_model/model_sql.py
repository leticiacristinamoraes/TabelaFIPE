from typing import List
import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, INT
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_model.db_base_postgresql import Base
class ModelsDBModel(Base):
    __tablename__ = 'Models'

    id: Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[String] = mapped_column(String)
    brand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Brands.id'))
    
    brand:  Mapped['BrandDBModel'] = relationship(back_populates='models')
    car:  Mapped['CarDBModel'] = relationship(back_populates='models')
