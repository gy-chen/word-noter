import os
from flask import Flask
from . import cors
from . import route
from . import model
from . import auth


def create_app(config_object=None, config_envvar=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)
    if os.environ.get(config_envvar):
        app.config.from_envvar(config_envvar)
    cors.init_app(app)
    route.init_app(app)
    model.init_app(app)
    auth.init_app(app)
    return app
