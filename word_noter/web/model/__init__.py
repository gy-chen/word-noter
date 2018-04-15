from .base import db
from .migrate import migrate
from .word import Word


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
