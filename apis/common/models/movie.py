from datetime import datetime

from sqlalchemy import UniqueConstraint

from apis.initialization import db


class Movie(db.Model):
    """ Movie Model for storing movie details"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ninety_nine_popularity = db.Column(db.Float, index=True, nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    director = db.Column(db.String(100), index=True, nullable=False)
    imdb_score = db.Column(db.Float, index=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (UniqueConstraint('name', 'director', name='move_name_director_name'),)

    # relations
    genres = db.relationship(
        'MovieGenre', backref='movie',
        primaryjoin='and_(MovieGenre.movie_id==Movie.id, MovieGenre.is_deleted==False)',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Movie %r>' % self.name


class MovieGenre(db.Model):
    """MovieGenre Model for genres of movie"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.name
