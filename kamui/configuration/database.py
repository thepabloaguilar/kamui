from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.declarative import declarative_base


_db_engine = create_engine(
    "postgresql+psycopg2://kamui:kamui@localhost:5432/kamui",
    poolclass=NullPool,
    echo=False,
)

_db_session = scoped_session(sessionmaker(bind=_db_engine))

DatabaseBase = declarative_base()
DatabaseBase.metadata.bind = _db_engine
DatabaseBase.query = _db_session.query_property()


def init_db() -> None:
    DatabaseBase.metadata.create_all(_db_engine)


@contextmanager
def database_session() -> Iterator[Session]:
    session = _db_session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
