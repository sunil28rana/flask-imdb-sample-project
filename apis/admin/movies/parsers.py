from flask_restplus import reqparse, ValidationError
from werkzeug.datastructures import FileStorage


def imdb_score():
    def validate(rating):
        if isinstance(float(rating), float) and 0 < float(rating) <= 10:
            return float(rating)
        raise ValidationError("Please provide a valid IMDB rating")

    return validate


def ninety_nine_popularity():
    def validate(rating):
        if isinstance(float(rating), float) and 0 < float(rating) <= 100:
            return float(rating)
        raise ValidationError("Please provide a valid 99popularity rating")

    return validate


add_movie_parser = reqparse.RequestParser(bundle_errors=True)
add_movie_parser.add_argument('name', type=str, required=True, help="Movies Name", location='form')
add_movie_parser.add_argument('director', type=str, required=True, help="Director Name of the movie", location='form')
add_movie_parser.add_argument('imdb_score', type=imdb_score(), required=True, help="IMDB rating of the movie",
                              location='form')
add_movie_parser.add_argument('ninety_nine_popularity', type=ninety_nine_popularity(), required=True,
                              help="99popularity rating", location='form')
add_movie_parser.add_argument('genres', type=str, action='append', required=True, help="List of movie genres",
                              location='form')

get_movie_parser = reqparse.RequestParser(bundle_errors=True, trim=True)
get_movie_parser.add_argument('name', type=str, default=None, help="Movie Name", location='args')
get_movie_parser.add_argument('director', type=str, default=None, help="Director Name of the movie", location='args')
get_movie_parser.add_argument('imdb_score', type=imdb_score(), default=None, help="IMDB rating of the movie",
                              location='args')
get_movie_parser.add_argument('ninety_nine_popularity', type=ninety_nine_popularity(), help="99popularity rating",
                              location='args')
get_movie_parser.add_argument('genres', type=str, action='append', default=None, help="List of movie genres",
                              location='args')
get_movie_parser.add_argument('offset', type=int, default=1)
get_movie_parser.add_argument('limit', type=int, default=20)

update_movie_parser = add_movie_parser.copy()
update_movie_parser.add_argument('is_deleted', type=bool, required=True, location='form')

movies_file_parser = reqparse.RequestParser(bundle_errors=True)
movies_file_parser.add_argument('file', type=FileStorage, required=True, help='Document file',
                                location='files')
