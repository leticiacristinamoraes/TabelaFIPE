from typing import List
import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, INT
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_model.db_base_postgresql import Base
class BrandDBModel(Base):
    __tablename__ = 'Brands'
    id: Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[String] = mapped_column(String)

    models: Mapped[List['ModelsDBModel']] = relationship(back_populates='brand')