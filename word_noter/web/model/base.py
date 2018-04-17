from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def model_to_dict(entity):
    return {key: value for key, value in entity.__dict__.items() if not key.startswith('_')}
