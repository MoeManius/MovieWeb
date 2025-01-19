from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datamanager.data_manager_interface import DataManagerInterface
from models import User, Movie

class SQLiteDataManager(DataManagerInterface):
    """SQLite implementation of the DataManagerInterface."""

    def __init__(self, app):
        """
        Initialize the SQLiteDataManager with a Flask app instance.
        :param app: The Flask app instance
        """
        self.db = SQLAlchemy(app)

    def get_all_users(self):
        """Retrieve all users from the database."""
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            print(f"Error retrieving all users: {e}")
            return []

    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Error retrieving user with ID {user_id}: {e}")
            return None

    def add_user(self, user):
        """Add a new user to the database."""
        try:
            self.db.session.add(user)
            self.db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error adding user: {e}")
            self.db.session.rollback()

    def get_user_movies(self, user_id):
        """Retrieve all movies for a specific user."""
        try:
            user = self.get_user_by_id(user_id)
            return user.movies if user else []
        except SQLAlchemyError as e:
            print(f"Error retrieving movies for user with ID {user_id}: {e}")
            return []

    def add_movie(self, user_id, movie):
        """Add a new movie to a user's list."""
        try:
            user = self.get_user_by_id(user_id)
            if user:
                movie.user_id = user_id
                self.db.session.add(movie)
                self.db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error adding movie for user with ID {user_id}: {e}")
            self.db.session.rollback()

    def update_movie(self, movie_id, updated_movie):
        """Update the details of a specific movie."""
        try:
            movie = self.get_movie_by_id(movie_id)
            if movie:
                movie.name = updated_movie.name
                movie.director = updated_movie.director
                movie.year = updated_movie.year
                movie.rating = updated_movie.rating
                self.db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error updating movie with ID {movie_id}: {e}")
            self.db.session.rollback()

    def delete_movie(self, movie_id):
        """Delete a specific movie from the database."""
        try:
            movie = self.get_movie_by_id(movie_id)
            if movie:
                self.db.session.delete(movie)
                self.db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error deleting movie with ID {movie_id}: {e}")
            self.db.session.rollback()

    def get_movie_by_id(self, movie_id):
        """Retrieve a movie by its ID."""
        try:
            return Movie.query.get(movie_id)
        except SQLAlchemyError as e:
            print(f"Error retrieving movie with ID {movie_id}: {e}")
            return None
