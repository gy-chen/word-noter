from flask import Flask
from . import cors
from . import route
from . import model


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    cors.init_app(app)
    route.init_app(app)
    model.init_app(app)
    return app


app = create_app('word_noter.web.config')

if __name__ == '__main__':
    app.run(debug=True)
