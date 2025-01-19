# MoviWeb App

MoviWeb is a Flask-based web application designed to manage users and their favorite movies. It allows users to:

- Register new users.
- Add and remove movies from their list of favorites.
- View their favorite movies.
- Interact with the app programmatically through API endpoints.

## Features

- **User Management**: Users can register with a unique username and view a list of all registered users.
- **Movie Management**: Users can add their favorite movies, view their list of movies, and remove movies from their list.
- **API**: The app exposes several API endpoints to interact with the app programmatically.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Running Tests](#running-tests)
- [License](#license)

## Installation

Follow these steps to install and run the MoviWeb app:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/moviweb-app.git
    cd moviweb-app
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv .venv
    ```

3. Activate the virtual environment:
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On MacOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. Set up environment variables:
    - Rename `.env.example` to `.env`.
    - Edit the `.env` file with your specific environment variables:
      - `FLASK_APP` = `app.py`
      - `FLASK_ENV` = `development` (or `production`)
      - `SQLALCHEMY_DATABASE_URI` = `sqlite:///movies.db` (or a different database URI)

## Usage

To start the Flask development server, use the following command:

```bash
python app.py

# URL
The app will be available at http://127.0.0.1:5000/.

Endpoints
Here are the key routes of the MovieWeb app:

User Routes:
GET /users: List all users.
POST /add_user: Add a new user.
    Form: username

GET /users/<user_id>/movies: List a user's favorite movies.
POST /users/<user_id>/movies: Add a new favorite movie for a user.
    Form: title, genre, rating

POST /users/<user_id>/delete_movie/<movie_id>: Remove a movie from a user's list.

API Routes:
GET /api/users: Get a list of all users.
POST /api/users: Add a new user.
    JSON: {"username": "username"}

GET /api/users/<user_id>/movies: Get a user's favorite movies.
POST /api/users/<user_id>/movies: Add a favorite movie for a user.
    JSON: {"title": "movie title", "genre": "movie genre", "rating": "movie rating"}

POST /api/users/<user_id>/delete_movie/<movie_id>: Remove a movie from a user's list.
    JSON: {"movie_id": "movie_id"}