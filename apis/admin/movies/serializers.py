from flask_restplus import fields

from apis.admin.admin_api import api

movie_ns = api.namespace('movies', description='Movie Module')


movie = movie_ns.model('Movie', {
    'id': fields.Integer(required=True, description='Movie id'),
    '99popularity': fields.Float(attribute='ninety_nine_popularity', required=True),
    'name': fields.String(required=True, description='Movie name'),
    'director': fields.String(required=True, description='Director name of the movie'),
    'imdb_score': fields.Float(required=True, description='IMDB rating of the movie'),
    'genres': fields.List(fields.String(attribute='name'))
})

movie_serializer = movie_ns.model('MovieSerializer', {
    'status': fields.Boolean(required=True),
    'data': fields.Nested(movie, skip_none=True),
    'message': fields.String(),
})


movies_serializer = movie_ns.model('MoviesSerializer', {
    'status': fields.Boolean(required=True),
    'message': fields.String(),
    'data': fields.List(fields.Nested(movie, skip_none=True), required=True)
})