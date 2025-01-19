import pytest
from app import app
from models import db, User, Movie


@pytest.fixture
def client():
    # Setup a temporary in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up the database after tests


def test_home_route(client):
    """Test the home route to ensure it renders the correct template"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'User List' in response.data  # Check that 'User List' appears in the response


def test_add_user(client):
    """Test the add user route (GET and POST)"""
    # Test GET request to show form
    response = client.get('/add_user')
    assert response.status_code == 200
    assert b'Add User' in response.data  # Check that the 'Add User' form is rendered

    # Test POST request to add a user
    response = client.post('/add_user', data={'name': 'Test User'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test User' in response.data  # Check that the newly added user is in the response


def test_user_movies(client):
    """Test viewing a user's movies"""
    # Create a test user and a test movie
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    movie = Movie(name="Test Movie", director="Test Director", year=2021, rating=5.0, user_id=user.id)
    db.session.add(movie)
    db.session.commit()

    # Test GET request to view the user's movies
    response = client.get(f'/user/{user.id}/movies')
    assert response.status_code == 200
    assert b'Test Movie' in response.data  # Check that the movie appears in the response


def test_add_movie(client):
    """Test adding a movie to a user"""
    # Create a test user
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    # Test GET request to show add movie form
    response = client.get(f'/user/{user.id}/movie/add')
    assert response.status_code == 200
    assert b'Add Movie' in response.data  # Check that the 'Add Movie' form is rendered

    # Test POST request to add a movie
    response = client.post(f'/user/{user.id}/movie/add',
                           data={'name': 'New Movie', 'director': 'Test Director', 'year': 2023, 'rating': 4.5},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'New Movie' in response.data  # Check that the new movie appears in the user's movie list


def test_update_movie(client):
    """Test updating a movie"""
    # Create a test user and movie
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    movie = Movie(name="Old Movie", director="Test Director", year=2021, rating=3.0, user_id=user.id)
    db.session.add(movie)
    db.session.commit()

    # Test GET request to show update form
    response = client.get(f'/user/{user.id}/movie/{movie.id}/edit')
    assert response.status_code == 200
    assert b'Edit Movie' in response.data  # Check that the 'Edit Movie' form is rendered

    # Test POST request to update the movie
    response = client.post(f'/user/{user.id}/movie/{movie.id}/edit',
                           data={'name': 'Updated Movie', 'director': 'Test Director', 'year': 2023, 'rating': 5.0},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Movie' in response.data  # Check that the updated movie appears in the user's movie list


def test_delete_movie(client):
    """Test deleting a movie"""
    # Create a test user and movie
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    movie = Movie(name="Movie to Delete", director="Test Director", year=2021, rating=3.0, user_id=user.id)
    db.session.add(movie)
    db.session.commit()

    # Test GET request to delete the movie
    response = client.get(f'/user/{user.id}/movie/{movie.id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Movie to Delete' not in response.data  # Check that the movie is no longer in the user's movie list


def test_user_not_found(client):
    """Test the behavior when trying to view a non-existent user's movies"""
    response = client.get('/user/999/movies')  # User ID 999 doesn't exist
    assert response.status_code == 404
    assert b'User not found' in response.data


def test_movie_not_found(client):
    """Test the behavior when trying to update or delete a non-existent movie"""
    # Create a test user
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/user/{user.id}/movie/999/edit')  # Movie ID 999 doesn't exist
    assert response.status_code == 404
    assert b'Movie not found' in response.data


def test_invalid_form_data(client):
    """Test the behavior of the add movie form with invalid data"""
    # Create a test user
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()

    # Test POST request with missing movie data
    response = client.post(f'/user/{user.id}/movie/add', data={'name': '', 'director': '', 'year': '', 'rating': ''},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid data' in response.data  # Adjust based on your form validation message
