from datetime import datetime
from typing import Optional, List

from sqlalchemy import and_

from apis.common.models import Movie, MovieGenre
from apis.initialization import db


def get_movie_by_id(movie_id: int) -> Movie or None:
    return Movie.query.get(movie_id)


def add_movie(name: str, director: str, ninety_nine_popularity: float, imdb_score: float, genres: List[str]) -> tuple:
    try:
        movie = Movie(
            name=name.title(),
            director=director.title(),
            imdb_score=round(imdb_score, 1),
            ninety_nine_popularity=round(ninety_nine_popularity, 1)
        )
        db.session.add(movie)
        db.session.flush()

        for genre in genres:
            movie_genre = MovieGenre(movie=movie, name=genre)
            db.session.add(movie_genre)
            db.session.flush()

        db.session.commit()
        return True, movie
    except Exception as e:
        # log error in file
        # print(e)
        db.session.rollback()
        return False, e


def update_movie(movie: Movie, name: str, director: str, ninety_nine_popularity: float, imdb_score: float, genres: List[str]) -> bool:
    try:
        movie.name = name.title()
        movie.director = director.title()
        movie.imdb_score = round(imdb_score, 1)
        movie.ninety_nine_popularity = round(ninety_nine_popularity, 1)
        movie.updated_at = datetime.utcnow()

        for genre in movie.genres:
            genre.is_deleted = True

        for genre in genres:
            movie_genre = MovieGenre(movie=movie, name=genre)
            db.session.add(movie_genre)
            db.session.flush()

        db.session.commit()
        return True
    except Exception as e:
        # log error in file
        print(e)
        db.session.rollback()
        return False


def delete_movie(movie_id: int) -> bool:
    try:
        movie = get_movie_by_id(movie_id)
        movie.is_deleted = True
        movie.updated_at = datetime.now()
        for genre in movie.genres:
            genre.is_deleted = True
        db.session.commit()
        return True
    except Exception as e:
        # log error in file
        print(e)
        db.session.rollback()
        return False


def get_movies(
        name: Optional[str] or None = None, director: Optional[str] = None,
        imdb_score: Optional[float] = None, ninety_nine_popularity: Optional[float] = None, genres: Optional[List[str]] = None,
        is_deleted: bool = False, offset: int = 1, limit: int = 20
) -> List[Movie]:
    movies = Movie.query

    if genres:
        movies = movies.filter(MovieGenre.name.in_(genres))
        movies = movies.join(
            MovieGenre, and_(
                MovieGenre.movie_id == Movie.id,
                MovieGenre.name.in_(genres),
                MovieGenre.is_deleted == is_deleted
            )
        )

    if name:
        movies = movies.filter(Movie.name.ilike('%{}%'.format(name)))

    if director:
        movies = movies.filter(Movie.director.ilike('%{}%'.format(director)))

    if imdb_score:
        movies = movies.filter(Movie.imdb_score >= imdb_score)

    if ninety_nine_popularity:
        movies = movies.filter(Movie.ninety_nine_popularity >= ninety_nine_popularity)

    movies = movies.filter(Movie.is_deleted == is_deleted)

    return movies.all()[(offset - 1):limit + (offset - 1)]
