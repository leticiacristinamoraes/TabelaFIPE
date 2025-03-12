from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class Base(DeclarativeBase):
    """ Base class for all models
    """
engine = create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/testDB')
Session = scoped_session(sessionmaker(bind=engine))

