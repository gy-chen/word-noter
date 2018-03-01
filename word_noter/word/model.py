import contextlib
import os
import sqlalchemy
import cerberus
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(os.environ.get("WORD_NOTER_DB", 'sqlite:///:memory:'), echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def model_to_dict(entity):
    return {key: value for key, value in entity.__dict__.items() if not key.startswith('_')}


@contextlib.contextmanager
def open_session():
    session = Session()
    yield session
    session.close()


class Word(Base):
    __tablename__ = 'words'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime)

    schema_for_add = {
        'name': {
            'type': 'string'
        }
    }

    @classmethod
    def put(cls, entity):
        v = cerberus.Validator(cls.schema_for_add)
        if not v.validate(entity):
            raise ValueError(v.errors)
        word = Word(**entity)
        word.date = datetime.now()
        with open_session() as session:
            session.add(word)
            wordDict = model_to_dict(word)
            session.commit()
            # XXX workaround for __dict__ cannot be accessed after session is commit.
            wordDict['id'] = word.id
        return wordDict

    @classmethod
    def get(cls, key):
        with open_session() as session:
            word = session.query(cls).filter(cls.id == key).one_or_none()
            return model_to_dict(word)

    @classmethod
    def delete(cls, key):
        with open_session() as session:
            word = session.query(cls).filter(cls.id == key).one_or_none()
            session.delete(word)
            session.commit()

    @classmethod
    def find_all(cls):
        with open_session() as session:
            return [model_to_dict(entity) for entity in session.query(cls).all()]


Base.metadata.create_all(engine)
