from apis.admin.movies.resources import Movie, Movies, MoviesFileUpload
from apis.admin.movies.serializers import movie_ns

movie_ns.add_resource(Movies, '/', methods=['GET', 'POST'])
movie_ns.add_resource(Movie, '/<int:id>', methods=['GET', 'PUT', 'DELETE'])
movie_ns.add_resource(MoviesFileUpload, '/upload-file', methods=['POST'])