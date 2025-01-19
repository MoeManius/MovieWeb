from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from datamanager.data_manager_interface import DataManagerInterface
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Set the database URI from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLiteDataManager with the Flask app's config
sqlite_data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    """Display all users"""
    users = sqlite_data_manager.get_all_users()
    return render_template('index.html', users=users)


@app.route('/user/<int:user_id>/movies')
def user_movies(user_id):
    """Display all movies for a specific user"""
    user = sqlite_data_manager.get_user_by_id(user_id)
    if user:
        movies = sqlite_data_manager.get_user_movies(user_id)
        return render_template('movie_list.html', user=user, movies=movies)
    else:
        return "User not found", 404


@app.route('/user/<int:user_id>/movie/add', methods=['GET', 'POST'])
def add_movie(user_id):
    """Add a new movie to a user's list"""
    user = sqlite_data_manager.get_user_by_id(user_id)
    if request.method == 'POST':
        movie_name = request.form['name']
        director = request.form['director']
        year = int(request.form['year'])
        rating = float(request.form['rating'])

        # Create a new movie object
        new_movie = {
            'name': movie_name,
            'director': director,
            'year': year,
            'rating': rating
        }

        # Add movie to the database
        sqlite_data_manager.add_movie(user_id, new_movie)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user)


@app.route('/user/<int:user_id>/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(user_id, movie_id):
    """Edit an existing movie"""
    movie = sqlite_data_manager.get_movie_by_id(user_id, movie_id)
    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        movie['name'] = request.form['name']
        movie['director'] = request.form['director']
        movie['year'] = int(request.form['year'])
        movie['rating'] = float(request.form['rating'])

        # Update the movie in the database
        sqlite_data_manager.update_movie(user_id, movie_id, movie)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('edit_movie.html', movie=movie)


@app.route('/user/<int:user_id>/movie/<int:movie_id>/delete')
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's list"""
    movie = sqlite_data_manager.get_movie_by_id(user_id, movie_id)
    if movie:
        sqlite_data_manager.delete_movie(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return "Movie not found", 404


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        name = request.form['name']
        new_user = {'name': name}

        # Add user to the database
        sqlite_data_manager.add_user(new_user)
        return redirect(url_for('home'))

    return render_template('add_user.html')


if __name__ == '__main__':
    app.run(debug=True)
