from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """An abstract interface that defines the methods a data manager must implement."""

    @abstractmethod
    def get_all_users(self):
        """Retrieve all users from the database."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    def add_user(self, user):
        """Add a new user to the database."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies for a specific user."""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie):
        """Add a new movie to a user's list."""
        pass

    @abstractmethod
    def update_movie(self, movie_id, updated_movie):
        """Update the details of a specific movie."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a specific movie from the database."""
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id):
        """Retrieve a movie by its ID."""
        pass
