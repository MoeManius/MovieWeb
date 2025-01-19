from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from api import api  # Import the API Blueprint

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///movieapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Register the API Blueprint to expose API endpoints
app.register_blueprint(api)

# Define models here or import from the models file
# from models import User, Movie

# Routes for main app
@app.route('/')
def index():
    return render_template('index.html')

# Additional routes (your other routes go here)
@app.route('/users')
def users():
    # Example logic for getting all users
    from models import User
    users = User.query.all()
    return render_template('users.html', users=users)

# Other routes for movies, user interaction, etc. go here
# You can define other routes like:
# - Add user
# - Add movie
# - Update movie
# - Delete movie
# and use SQLAlchemy to interact with the database

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle other HTTP errors
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
