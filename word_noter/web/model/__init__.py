from .base import db, migrate
from .word import Word
from .user import User


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
