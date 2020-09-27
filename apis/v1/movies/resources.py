from flask_restplus import Resource

from apis.admin.movies.parsers import get_movie_parser
from apis.v1.movies.serializers import movie_ns, movies_serializer, movie_serializer
from apis.common.business.movie import get_movie_by_id, get_movies


class Movie(Resource):
    @movie_ns.marshal_with(movie_serializer)
    def get(self, id):
        """Get a movie by it's id"""
        movie = get_movie_by_id(movie_id=id)
        if movie is None:
            return {
                       'status': False,
                       'message': "Couldn't find a movie with id {}".format(id)
                   }, 404

        return {
            'status': True,
            'data': movie
        }


class Movies(Resource):
    @movie_ns.marshal_with(movies_serializer)
    @movie_ns.expect(get_movie_parser)
    def get(self):
        """Get all movies"""
        data = get_movie_parser.parse_args()
        return {
                   'status': True,
                   'data': get_movies(**data)
               }, 200
