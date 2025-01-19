from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
from models import User, Movie

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app=None):
        # Initialize the SQLAlchemy object
        self.db = SQLAlchemy()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the app with SQLAlchemy"""
        self.db.init_app(app)

    def get_all_users(self):
        """Fetch all users from the database"""
        return User.query.all()

    def get_user_by_id(self, user_id):
        """Fetch a user by ID from the database"""
        return User.query.get(user_id)

    def get_user_movies(self, user_id):
        """Fetch all movies for a specific user"""
        user = User.query.get(user_id)
        if user:
            return user.movies  # Assuming a relationship exists between User and Movie
        return []

    def add_user(self, user_data):
        """Add a new user to the database"""
        user = User(name=user_data['name'])
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, user_id, movie_data):
        """Add a new movie to a user's list"""
        user = User.query.get(user_id)
        if user:
            movie = Movie(
                name=movie_data['name'],
                director=movie_data['director'],
                year=movie_data['year'],
                rating=movie_data['rating'],
                user_id=user_id  # Assuming a foreign key relationship exists
            )
            self.db.session.add(movie)
            self.db.session.commit()

    def update_movie(self, user_id, movie_id, movie_data):
        """Update an existing movie"""
        movie = Movie.query.get(movie_id)
        if movie and movie.user_id == user_id:
            movie.name = movie_data['name']
            movie.director = movie_data['director']
            movie.year = movie_data['year']
            movie.rating = movie_data['rating']
            self.db.session.commit()

    def delete_movie(self, user_id, movie_id):
        """Delete a movie from the database"""
        movie = Movie.query.get(movie_id)
        if movie and movie.user_id == user_id:
            self.db.session.delete(movie)
            self.db.session.commit()

    def get_movie_by_id(self, user_id, movie_id):
        """Fetch a specific movie by ID"""
        return Movie.query.filter_by(user_id=user_id, id=movie_id).first()
