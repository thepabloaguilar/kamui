from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


_db_engine = create_engine("sqlite:///kamui.sqlite", poolclass=NullPool, echo=False,)

_db_session = scoped_session(sessionmaker(bind=_db_engine))

DatabaseBase = declarative_base()
DatabaseBase.metadata.bind = _db_engine
DatabaseBase.query = _db_session.query_property()
