from datetime import datetime
import cerberus
from .base import db


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.TIMESTAMP(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='words')

    schema_for_add = {
        'name': {
            'type': 'string',
            'required': True
        },
        'user': {
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
        word.user = entity.user
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
    def find_by_user(cls, user):
        return cls.query.filter_by(user=user).all()

    @classmethod
    def find_by_id_and_user(cls, id_, user):
        return cls.query.filter_by(id=id_, user=user).one()

    @classmethod
    def find_all(cls):
        return [entity for entity in cls.query.all()]
