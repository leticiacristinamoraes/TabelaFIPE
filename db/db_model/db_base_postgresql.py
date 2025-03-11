from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine



class Base(DeclarativeBase):
    """ Base class for all models
    """
    engine = create_engine('config.DB_URI')
    Session = scoped_session(sessionmaker(bind=engine))