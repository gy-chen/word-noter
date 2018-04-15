from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#def model_to_dict(entity):
#    return {key: value for key, value in entity.__dict__.items() if not key.startswith('_')}
