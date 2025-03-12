import datetime
from typing import List
import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, func

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db.db_model.db_base_postgresql import Base

class RegisterDBModel(Base):
    __tablename__ = 'Registers'
    
    id: Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Shops.id'))
    car_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Cars.id'))
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    price: Mapped[String] = mapped_column(String)

    shops: Mapped[List['ShopDBModel']] = relationship( back_populates='registers')
    cars: Mapped[List['CarDBModel']] = relationship(back_populates='registers')