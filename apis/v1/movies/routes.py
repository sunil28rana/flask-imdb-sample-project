from apis.v1.movies.resources import Movie, Movies
from apis.v1.movies.serializers import movie_ns

movie_ns.add_resource(Movies, '/', methods=['GET', 'POST'])
movie_ns.add_resource(Movie, '/<int:id>', methods=['GET', 'PUT', 'DELETE'])
