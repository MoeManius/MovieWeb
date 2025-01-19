from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationship to movies through UserMovie (Many-to-Many)
    movies = db.relationship('Movie', secondary='user_movie', back_populates="users")

    # Relationship to reviews (One-to-Many)
    reviews = db.relationship('Review', backref='user', lazy=True)


class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100))
    rating = db.Column(db.Float)
    release_year = db.Column(db.Integer)

    # Relationship to users through UserMovie (Many-to-Many)
    users = db.relationship('User', secondary='user_movie', back_populates="movies")

    # Relationship to reviews (One-to-Many)
    reviews = db.relationship('Review', backref='movie', lazy=True)


class UserMovie(db.Model):
    __tablename__ = 'user_movie'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)


class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, user_id, movie_id, review_text, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.review_text = review_text
        self.rating = rating
