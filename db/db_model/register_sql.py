import uuid
from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from db.db_model.db_base_postgresql import Base

class RegisterDBModel(Base):
    __tablename__ = 'Registers'
    id = Column(uuid.UUID, primary_key=True)
    shop_id = Column(uuid.UUID, ForeignKey('Shops.id'))
    car_id = Column(uuid.UUID, ForeignKey('Cars.id'))
    created_date = Column(Date)
    price = Column(String)
    shop = relationship("Shop")
    car = relationship("Car")