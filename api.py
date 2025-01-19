from flask import Blueprint, jsonify, request
from models import db, User, Movie

# Initialize the Blueprint for API routes
api = Blueprint('api', __name__)


# Get all users
@api.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []

    # Iterate over each user and format the response
    for user in users:
        user_list.append({
            'user_id': user.user_id,
            'username': user.username
        })

    # Return the list of users as JSON
    return jsonify(user_list)


# Get a user's favorite movies
@api.route('/api/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = User.query.get_or_404(user_id)  # Get the user by ID or return 404
    movies = user.movies  # Assuming a relationship between User and Movie
    movie_list = []

    # Iterate over each movie and format the response
    for movie in movies:
        movie_list.append({
            'movie_id': movie.movie_id,
            'title': movie.title,
            'genre': movie.genre,
            'rating': movie.rating
        })

    # Return the list of movies as JSON
    return jsonify(movie_list)


# Add a movie to a user's favorite movies
@api.route('/api/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    user = User.query.get_or_404(user_id)  # Get the user by ID or return 404

    # Get JSON data from the request
    data = request.get_json()

    # Validate required fields in the request data
    if 'title' not in data or 'genre' not in data or 'rating' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new Movie object
    new_movie = Movie(
        title=data['title'],
        genre=data['genre'],
        rating=data['rating'],
        user_id=user.user_id
    )

    # Add the new movie to the session and commit to the database
    db.session.add(new_movie)
    db.session.commit()

    # Return the newly created movie as JSON
    return jsonify({
        'movie_id': new_movie.movie_id,
        'title': new_movie.title,
        'genre': new_movie.genre,
        'rating': new_movie.rating
    }), 201


# Error handling for 404 errors (Resource not found)
@api.app_errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404


# Error handling for invalid input (400 Bad Request)
@api.app_errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad Request'}), 400

