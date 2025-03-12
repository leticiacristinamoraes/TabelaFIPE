import uuid
from sqlalchemy import Column, String
from db.db_model.db_base_postgresql import Base

class RoleDBModel(Base):
    __tablename__ = 'Roles'
    id = Column(uuid.UUID, primary_key=True)
    name = Column(String)
