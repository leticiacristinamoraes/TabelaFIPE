import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from db.db_model.db_base_postgresql import Base

class UserRoleDBModel(Base):
    __tablename__ = 'Users_roles'
    id = Column(uuid.UUID, primary_key=True)
    user_id = Column(uuid.UUID, ForeignKey('Users.id'))
    role_id = Column(uuid.UUID, ForeignKey('Roles.id'))
    user = relationship("User")
    role = relationship("Role")