from typing import List
import uuid
from sqlalchemy import UUID, Column, String

from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_model.db_base_postgresql import Base

class ShopDBModel(Base):
    __tablename__ = 'Shops'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[String] = mapped_column(String)

    registers: Mapped[List['RegisterDBModel']] = relationship(back_populates='shops')
