from flask import request
from flask_restful import Api, Resource, marshal_with, fields, reqparse, abort
from ..model import Word
from ..auth import require_login, current_user

api = Api()

word_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'date': fields.DateTime
}


class WordResource(Resource):
    """Word RestFul API

    """

    @marshal_with(word_fields)
    @require_login
    def get(self, id_):
        word = Word.find_by_id_and_user(id_, current_user)
        return word


class WordListResource(Resource):
    """Display words list

    """

    @marshal_with(word_fields)
    @require_login
    def get(self):
        words = Word.find_by_user(current_user)
        return words

    @marshal_with(word_fields)
    @require_login
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        word = parser.parse_args()
        word['user'] = current_user
        try:
            return Word.put(word)
        except ValueError as e:
            return abort(400, message=e.args[0])


def init_app(app):
    api.add_resource(WordListResource, '/words')
    api.add_resource(WordResource, '/words/<id_>')
    api.init_app(app)
