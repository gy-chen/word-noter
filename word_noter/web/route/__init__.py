from . import word
from . import auth


def init_app(app):
    word.init_app(app)
    auth.init_app(app)
