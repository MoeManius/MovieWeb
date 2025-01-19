from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Fetch all users"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Fetch all movies for a specific user"""
        pass

    @abstractmethod
    def add_user(self, user):
        """Add a new user"""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie):
        """Add a movie to a user's movie list"""
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, movie):
        """Update an existing movie's details"""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Delete a movie from a user's movie list"""
        pass

    @abstractmethod
    def get_movie_by_id(self, user_id, movie_id):
        """Fetch a specific movie by its ID"""
        pass
