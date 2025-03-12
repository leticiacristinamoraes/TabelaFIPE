import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from db.db_model.db_base_postgresql import Base


class AvgPriceDBModel(Base):
    __tablename__ = 'Avg_price'
    id = Column(uuid.UUID, primary_key=True)
    car_id = Column(uuid.UUID, ForeignKey('Cars.id'))
    avg_price = Column(String)
    car = relationship("Car")
    