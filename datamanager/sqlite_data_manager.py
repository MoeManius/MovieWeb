from datamanager.datamanager_interface import DataManagerInterface
from models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app, db_file_name):
        # Initialize the Flask app and set up SQLAlchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        self.app = app
        self.db = db

    def get_all_users(self):
        """Fetch all users from the database"""
        users = User.query.all()  # Using SQLAlchemy ORM to query all users
        return users

    def get_user_movies(self, user_id):
        """Fetch all movies for a given user from the database"""
        user = User.query.get(user_id)
        if user:
            return user.movies  # Using relationship to get all movies of the user
        else:
            return []

    def add_user(self, user):
        """Add a new user to the database"""
        db.session.add(user)  # Add the user instance to the session
        db.session.commit()  # Commit to save the user in the database

    def add_movie(self, user_id, movie):
        """Add a new movie for a user"""
        user = User.query.get(user_id)
        if user:
            user.movies.append(movie)  # Add movie to the user's movies list
            db.session.commit()  # Commit the transaction
        else:
            raise ValueError(f"User with ID {user_id} does not exist")

    def update_movie(self, user_id, movie_id, movie):
        """Update a movie's details in the database"""
        movie_to_update = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if movie_to_update:
            movie_to_update.name = movie.name
            movie_to_update.director = movie.director
            movie_to_update.year = movie.year
            movie_to_update.rating = movie.rating
            db.session.commit()  # Commit the transaction
        else:
            raise ValueError(f"Movie with ID {movie_id} for User {user_id} not found")

    def delete_movie(self, user_id, movie_id):
        """Delete a specific movie from the user's list"""
        movie_to_delete = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if movie_to_delete:
            db.session.delete(movie_to_delete)  # Remove the movie from the session
            db.session.commit()  # Commit the transaction
        else:
            raise ValueError(f"Movie with ID {movie_id} for User {user_id} not found")

    def get_movie_by_id(self, user_id, movie_id):
        """Fetch a specific movie for a user"""
        return Movie.query.filter_by(id=movie_id, user_id=user_id).first()
