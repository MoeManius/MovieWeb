from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Retrieve all users from the data source."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies for a given user from the data source."""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie):
        """Add a new movie for a specific user."""
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, updated_movie):
        """Update a movie's information for a specific user."""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Delete a specific movie from a user's list."""
        pass

    @abstractmethod
    def get_movie_by_id(self, user_id, movie_id):
        """Retrieve a specific movie by its ID for a given user."""
        pass
