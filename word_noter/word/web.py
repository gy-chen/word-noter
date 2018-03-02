from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields
from flask_cors import CORS
from word_noter.word.model import Word

app = Flask(__name__)
CORS(app)
api = Api(app)

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
    def get(self, id_):
        word = Word.get(id_)
        return word


class WordsResource(Resource):
    """Display words list

    """

    @marshal_with(word_fields)
    def get(self):
        words = Word.find_all()
        return words

    @marshal_with(word_fields)
    def post(self):
        word = {
            'name': request.form.get('name', None)
        }
        try:
            return Word.put(word)
        except ValueError as e:
            return {'error': e.args[0]}, 400


api.add_resource(WordsResource, '/words')
api.add_resource(WordResource, '/words/<id_>')

if __name__ == '__main__':
    app.run(debug=True)
