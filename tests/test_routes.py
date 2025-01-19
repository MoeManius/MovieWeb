import pytest
from app import app, db
from models import User, Movie
from flask import jsonify

@pytest.fixture
def client():
    with app.test_client() as client:
        # Ensure the database is set up before each test
        with app.app_context():
            db.create_all()
        yield client
        # Cleanup after tests
        with app.app_context():
            db.drop_all()

# Test Route Functionality: Adding and getting users

def test_add_user(client):
    # Create a new user
    response = client.post('/add_user', data={
        'username': 'test_user'
    })
    assert response.status_code == 200
    assert b'User added successfully' in response.data

def test_get_users(client):
    # Add a user
    client.post('/add_user', data={'username': 'test_user'})

    # Retrieve users
    response = client.get('/users')
    assert response.status_code == 200
    assert b'test_user' in response.data

def test_get_user_movies(client):
    # Add user and movie
    client.post('/add_user', data={'username': 'test_user'})
    response = client.post('/users/1/add_movie', data={
        'title': 'Inception',
        'genre': 'Sci-Fi',
        'rating': '8.8'
    })

    assert response.status_code == 200
    response = client.get('/users/1/movies')
    assert response.status_code == 200
    assert b'Inception' in response.data

# Test Route for Invalid Cases

def test_get_non_existing_user(client):
    response = client.get('/users/999/movies')
    assert response.status_code == 404
    assert b'User not found' in response.data

def test_get_non_existing_movie(client):
    client.post('/add_user', data={'username': 'test_user'})
    response = client.get('/users/1/movie/999')
    assert response.status_code == 404
    assert b'Movie not found' in response.data

# Test Movie Persistence After Restart

def test_movie_persistence(client):
    # Add user and movie
    client.post('/add_user', data={'username': 'test_user'})
    client.post('/users/1/add_movie', data={
        'title': 'The Matrix',
        'genre': 'Sci-Fi',
        'rating': '9.0'
    })

    # Restart the client to simulate server restart
    with app.app_context():
        db.session.remove()

    # Check if movie is still there
    response = client.get('/users/1/movies')
    assert response.status_code == 200
    assert b'The Matrix' in response.data

# Test Form Validation

def test_add_movie_invalid_form(client):
    # Try adding a movie with an invalid form (empty fields)
    response = client.post('/users/1/add_movie', data={})
    assert response.status_code == 400
    assert b'Invalid input' in response.data

# Test Edge Cases for Missing Parameters

def test_add_user_invalid_data(client):
    response = client.post('/add_user', data={})
    assert response.status_code == 400
    assert b'Username is required' in response.data

# Test Deleting a Movie

def test_delete_movie(client):
    # Add user and movie
    client.post('/add_user', data={'username': 'test_user'})
    client.post('/users/1/add_movie', data={
        'title': 'The Dark Knight',
        'genre': 'Action',
        'rating': '9.0'
    })

    # Delete movie
    response = client.post('/users/1/delete_movie/1')
    assert response.status_code == 200
    assert b'Movie deleted successfully' in response.data

    # Try retrieving deleted movie
    response = client.get('/users/1/movies')
    assert b'The Dark Knight' not in response.data

# Test API Endpoints

def test_api_add_movie(client):
    response = client.post('/api/users/1/movies', json={
        'title': 'Interstellar',
        'genre': 'Sci-Fi',
        'rating': '8.6'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Interstellar'

def test_api_get_user_movies(client):
    # Add user and movie through API
    client.post('/api/users', json={'username': 'test_user'})
    client.post('/api/users/1/movies', json={
        'title': 'Interstellar',
        'genre': 'Sci-Fi',
        'rating': '8.6'
    })

    response = client.get('/api/users/1/movies')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Interstellar'

def test_api_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Ensures the response is a list of users

