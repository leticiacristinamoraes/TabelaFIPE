from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

#CLasse usada como super classe. Ela permite criar as tabelas no banco de dados..
class Base(DeclarativeBase):
    """ Base class for all models
    """
    pass

