import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datamanager.sqlite_data_manager import SQLiteDataManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")  # Database URI from .env
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")  # Default secret key if not in .env
db = SQLAlchemy(app)

# Initialize SQLiteDataManager
sqlite_data_manager = SQLiteDataManager(db)

# Set up logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 error (Page Not Found)"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 error (Internal Server Error)"""
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected exceptions"""
    logging.error(f"Unhandled exception: {str(e)}")
    return render_template('500.html'), 500

# Routes
@app.route('/')
def home():
    """Home page showing all users"""
    try:
        users = sqlite_data_manager.get_all_users()
        return render_template('index.html', users=users)
    except Exception as e:
        logging.error(f"Error in home route: {str(e)}")
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """Display a user's favorite movies"""
    try:
        user = sqlite_data_manager.get_user_by_id(user_id)
        if not user:
            flash("User not found!", "error")
            return redirect(url_for('home'))
        return render_template('movie_list.html', user=user)
    except Exception as e:
        logging.error(f"Error in user_movies route for user_id={user_id}: {str(e)}")
        return render_template('500.html'), 500

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        try:
            username = request.form['username']
            if not username:
                flash("Username cannot be empty!", "error")
                return redirect(url_for('add_user'))
            sqlite_data_manager.add_user({'name': username})
            flash("User added successfully!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            logging.error(f"Error in add_user route: {str(e)}")
            return render_template('500.html'), 500
    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Add a movie to a user's favorite list"""
    if request.method == 'POST':
        try:
            title = request.form['title']
            if not title:
                flash("Movie title cannot be empty!", "error")
                return redirect(url_for('add_movie', user_id=user_id))
            movie_data = {'title': title}
            sqlite_data_manager.add_movie(user_id, movie_data)
            flash("Movie added successfully!", "success")
            return redirect(url_for('user_movies', user_id=user_id))
        except Exception as e:
            logging.error(f"Error in add_movie route for user_id={user_id}: {str(e)}")
            return render_template('500.html'), 500
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Update a movie's details"""
    try:
        if request.method == 'POST':
            updated_data = {
                'title': request.form['title'],
                'rating': request.form['rating']
            }
            sqlite_data_manager.update_movie(user_id, movie_id, updated_data)
            flash("Movie updated successfully!", "success")
            return redirect(url_for('user_movies', user_id=user_id))
        movie = sqlite_data_manager.get_movie_by_id(movie_id)
        if not movie:
            flash("Movie not found!", "error")
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('edit_movie.html', movie=movie)
    except Exception as e:
        logging.error(f"Error in update_movie route for user_id={user_id}, movie_id={movie_id}: {str(e)}")
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's list"""
    try:
        sqlite_data_manager.delete_movie(movie_id)
        flash("Movie deleted successfully!", "success")
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        logging.error(f"Error in delete_movie route for user_id={user_id}, movie_id={movie_id}: {str(e)}")
        return render_template('500.html'), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
