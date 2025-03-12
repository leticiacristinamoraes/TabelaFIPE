import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db.db_model.car_sql import CarDBModel
from db.db_model.db_base_postgresql import Base


class AvgPriceDBModel(Base):
    __tablename__ = 'Avg_price'

    id: Mapped[uuid.UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    car_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Cars.id'))
    avg_price: Mapped[String] = mapped_column(String)
    
    car: Mapped[CarDBModel] = relationship(back_populates='avg_price')
    