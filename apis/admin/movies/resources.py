import json
import os
from uuid import uuid4

from flask import current_app
from flask_restplus import Resource
from sqlalchemy.orm import Session

from apis.admin.movies.parsers import add_movie_parser, get_movie_parser, update_movie_parser, movies_file_parser
from apis.admin.movies.serializers import movie_ns, movies_serializer, movie_serializer
from apis.common.business.movie import get_movie_by_id, get_movies, update_movie, delete_movie, add_movie
from apis.common.helpers import authorization_required
from apis.common.models import MovieGenre, Movie as MovieModel
from apis.initialization import db


class Movie(Resource):
    @movie_ns.doc(security="Authorization")
    @authorization_required
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

    @movie_ns.doc(security="Authorization")
    @movie_ns.expect(update_movie_parser)
    @authorization_required
    def put(self, id):
        """Update a movie by it's id"""
        movie = get_movie_by_id(movie_id=id)
        data = update_movie_parser.parse_args()
        if movie is None:
            return {
                       'status': False,
                       'message': "Couldn't find a movie with id {}".format(id)
                   }, 404
        if update_movie(movie=movie, **data):
            return {
                       'status': True,
                       'message': "Movie updated!"
                   }, 200
        return {
                   'status': False,
                   'message': "Something went wrong"
               }, 500

    @movie_ns.doc(security="Authorization")
    @authorization_required
    def delete(self, id):
        """Delete a movie by it's id"""
        movie = get_movie_by_id(movie_id=id)
        if movie is None:
            return {
                       'status': False,
                       'message': "Couldn't find a movie with id {}".format(id)
                   }, 404
        if delete_movie(movie_id=movie.id):
            return {
                       'status': True,
                       'message': "Movie deleted!"
                   }, 202


class Movies(Resource):
    @movie_ns.doc(security="Authorization")
    @movie_ns.marshal_with(movies_serializer)
    @movie_ns.expect(get_movie_parser)
    @authorization_required
    def get(self):
        """Get all movies"""
        data = get_movie_parser.parse_args()
        return {
                   'status': True,
                   'data': get_movies(**data)
               }, 200

    @movie_ns.doc(security="Authorization")
    @movie_ns.expect(add_movie_parser)
    @movie_ns.marshal_with(movie_serializer)
    @authorization_required
    def post(self):
        """Add a new movie"""
        data = add_movie_parser.parse_args()
        status, object = add_movie(**data)
        if status:
            return {
                       'status': True,
                       'message': "Movie added!",
                       'data': object
                   }, 201
        return {
                   'status': False,
                   'message': object.__str__()
               }, 500


class MoviesFileUpload(Resource):
    # @movie_ns.doc(security="Authorization")
    @movie_ns.expect(movies_file_parser)
    # @authorization_required
    def post(self):
        """Upload json file into the database"""
        data = movies_file_parser.parse_args()
        file = data.file

        if file.mimetype != 'application/json':
            return {
                'status': False,
                'message': 'Only JSON files are allowed!'
            }

        temp_dir = current_app.config['TEMP_DIR']

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        filename = str(uuid4())
        file.save(temp_dir + filename)

        with open(temp_dir + filename, 'r') as file:
            file_dict = json.loads(file.read())

        movies_object = list()
        movie_genre_object = list()
        if len(file_dict) > 0:
            db.session.execute('''DELETE FROM movie''')
            db.session.execute('''DELETE FROM movie_genre''')
            db.session.commit()

            for row in file_dict:
                movie = MovieModel(
                    name=row['name'].title(),
                    director=row['director'].title(),
                    imdb_score=row['imdb_score'],
                    ninety_nine_popularity=row['99popularity']
                )
                db.session.add(movie)
                db.session.flush()

                for genre in row['genre']:
                    movie_genre = MovieGenre(movie=movie, name=genre)
                    db.session.add(movie_genre)
                    db.session.flush()


            db.session.commit()

        return {
                   'status': True,
                   'message': 'File uploaded successfully!'
               }, 200
