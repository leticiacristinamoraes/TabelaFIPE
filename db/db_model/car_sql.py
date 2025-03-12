import uuid
from sqlalchemy import Column, String
from db.db_model.db_base_postgresql import Base

class CarDBModel(Base):
    __tablename__ = 'Cars'
    id = Column(uuid.UUID, primary_key=True)
    brand = Column(String)
    model = Column(String)
    model_year = Column(String)
