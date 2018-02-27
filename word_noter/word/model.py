import contextlib
import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(os.environ.get("WORD_NOTER_DB", 'sqlite:///:memory:'), echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


@contextlib.contextmanager
def get_session():
    session = Session()
    yield session
    session.close()


class Word(Base):
    __tablename__ = 'words'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime)


Base.metadata.create_all(engine)
