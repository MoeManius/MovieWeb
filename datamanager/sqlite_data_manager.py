from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface

# Initialize the database
db = SQLAlchemy()

class User(db.Model):
    """Define the User model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship with movies
    movies = db.relationship('Movie', backref='user', lazy=True)


class Movie(db.Model):
    """Define the Movie model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app, db_file_name):
        self.app = app
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

    # 1. Get all users
    def get_all_users(self):
        return User.query.all()

    # 2. Get all movies for a specific user
    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    # 3. Add a new user (static method)
    @staticmethod
    def add_user(user):
        db.session.add(user)
        db.session.commit()

    # 4. Add a new movie
    def add_movie(self, user_id, movie):
        movie.user_id = user_id  # Associate the movie with the user
        db.session.add(movie)
        db.session.commit()

    # 5. Update a movie's details
    def update_movie(self, user_id, movie_id, updated_movie):
        movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
        if movie:
            movie.name = updated_movie.name
            movie.director = updated_movie.director
            movie.year = updated_movie.year
            movie.rating = updated_movie.rating
            db.session.commit()

    # 6. Delete a movie
    def delete_movie(self, user_id, movie_id):
        movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
        if movie:
            db.session.delete(movie)
            db.session.commit()

    # 7. Get a movie by its ID for a specific user
    def get_movie_by_id(self, user_id, movie_id):
        return Movie.query.filter_by(user_id=user_id, id=movie_id).first()
