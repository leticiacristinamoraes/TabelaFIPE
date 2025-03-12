from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable


class Base(DeclarativeBase):
    """ Base class for all models
    """
    pass

