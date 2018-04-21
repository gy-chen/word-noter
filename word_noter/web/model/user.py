from .base import db, model_to_dict


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)

    words = db.relationship('Word', back_populates='user')

    @classmethod
    def create_or_update(cls, user_info):
        user = cls.query.get(user_info['sub']) or User()
        user.id = user_info['sub']
        user.name = user_info['name']
        user.picture = user_info['picture']
        user.email = user_info['email']
        db.session.add(user)
        db.session.commit()
        return user

    def to_dict(self):
        return model_to_dict(self)
