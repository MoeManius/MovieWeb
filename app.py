from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from models import db, User, Movie

app = Flask(__name__)

# Initialize SQLiteDataManager with the database file
sqlite_data_manager = SQLiteDataManager(app, "movieweb.db")

# Home Route - Display all users
@app.route('/')
def home():
    """Display all users"""
    users = sqlite_data_manager.get_all_users()
    return render_template('index.html', users=users)

# User Movies Route - Display all movies for a specific user
@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """Display all movies for a specific user"""
    user = User.query.get(user_id)
    if user:
        movies = sqlite_data_manager.get_user_movies(user_id)
        return render_template('movie_list.html', user=user, movies=movies)
    else:
        return "User not found", 404

# Add User Route - Display form to add a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add a new user to the app"""
    if request.method == 'POST':
        user_name = request.form['name']
        new_user = User(name=user_name)  # Create a new user instance
        sqlite_data_manager.add_user(new_user)
        return redirect(url_for('home'))  # Redirect to home after adding the user

    return render_template('add_user.html')  # Display the form to add a new user

# Add Movie Route - Display form to add a new movie to a user's list
@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Add a new movie to a user's list"""
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        movie_name = request.form['name']
        director = request.form['director']
        year = int(request.form['year'])
        rating = float(request.form['rating'])

        # Create a new movie instance
        new_movie = Movie(name=movie_name, director=director, year=year, rating=rating)

        # Add movie to the database
        sqlite_data_manager.add_movie(user_id, new_movie)
        return redirect(url_for('user_movies', user_id=user_id))  # Redirect to user's movie list

    return render_template('add_movie.html', user=user)  # Display the form to add a movie

# Update Movie Route - Display form to update movie details
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Update an existing movie's details"""
    movie = sqlite_data_manager.get_movie_by_id(user_id, movie_id)
    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.director = request.form['director']
        movie.year = int(request.form['year'])
        movie.rating = float(request.form['rating'])

        # Update the movie in the database
        sqlite_data_manager.update_movie(user_id, movie_id, movie)
        return redirect(url_for('user_movies', user_id=user_id))  # Redirect back to the user's movie list

    return render_template('edit_movie.html', movie=movie)  # Display the form to edit a movie

# Delete Movie Route - Delete a specific movie from a user's list
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    """Delete a movie from the user's list"""
    movie = sqlite_data_manager.get_movie_by_id(user_id, movie_id)
    if movie:
        sqlite_data_manager.delete_movie(user_id, movie_id)  # Delete the movie from the database
        return redirect(url_for('user_movies', user_id=user_id))  # Redirect to the user's movie list
    else:
        return "Movie not found", 404

if __name__ == '__main__':
    app.run(debug=True)
