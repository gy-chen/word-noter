from datetime import datetime
import cerberus
from .base import db


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.DateTime)

    schema_for_add = {
        'name': {
            'type': 'string',
            'required': True
        }
    }

    @classmethod
    def put(cls, entity):
        v = cerberus.Validator(cls.schema_for_add)
        if not v.validate(entity):
            raise ValueError(v.errors)
        word = Word(**entity)
        word.date = datetime.now()
        db.session.add(word)
        db.session.commit()
        return word

    @classmethod
    def get(cls, key):
        word = cls.query.filter(cls.id == key).one_or_none()
        return word

    @classmethod
    def delete(cls, key):
        word = cls.query.filter(cls.id == key).one_or_none()
        db.session.delete(word)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return [entity for entity in cls.query.all()]
