import pytest
from app import app, db, Movie, Actor

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# Tests for /movies endpoint
def test_get_movies_success(client):
    with app.app_context():
        movie = Movie(title="Test Movie", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
    response = client.get('/movies')
    assert response.status_code == 200
    assert response.json['success'] is True
    assert len(response.json['movies']) == 1

def test_get_movies_not_found(client):
    response = client.get('/movies')
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'No movies found!' in response.json['message']

# Tests for /movies/<int:movie_id> endpoint
def test_get_movie_success(client):
    with app.app_context():
        movie = Movie(title="Test Movie", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id  # Access the ID while the session is active
    response = client.get(f'/movies/{movie_id}')
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['movie']['title'] == "Test Movie"

def test_get_movie_not_found(client):
    response = client.get('/movies/1')
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'Movie not found with the provided ID.' in response.json['message']

# Tests for /movies POST endpoint
def test_create_movie_success(client):
    response = client.post('/movies', json={'title': 'New Movie', 'release_date': '2023-01-01'})
    assert response.status_code == 201
    assert response.json['success'] is True
    assert response.json['movie']['title'] == 'New Movie'

def test_create_movie_invalid_input(client):
    response = client.post('/movies', json={'title': 'New Movie'})
    assert response.status_code == 400
    assert response.json['success'] is False
    assert 'Missing required fields' in response.json['message']

# Tests for /movies/<int:movie_id> PUT endpoint
def test_update_movie_success(client):
    with app.app_context():
        movie = Movie(title="Old Title", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id  # Access the ID while the session is active
    response = client.put(f'/movies/{movie_id}', json={'title': 'Updated Title', 'release_date': '2023-01-02'})
    assert response.status_code == 201
    assert response.json['success'] is True
    assert response.json['movie']['title'] == 'Updated Title'

def test_update_movie_not_found(client):
    response = client.put('/movies/1', json={'title': 'Updated Title', 'release_date': '2023-01-02'})
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'Movie not found with the provided ID.' in response.json['message']

# Tests for /movies/<int:movie_id> DELETE endpoint
def test_delete_movie_success(client):
    with app.app_context():
        movie = Movie(title="Test Movie", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id  # Access the ID while the session is active
    response = client.delete(f'/movies/{movie_id}')
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'Movie deleted successfully!' in response.json['message']

def test_delete_movie_not_found(client):
    response = client.delete('/movies/1')
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'Movie not found with the provided ID.' in response.json['message']

# Tests for /actors endpoint
def test_get_actors_success(client):
    with app.app_context():
        actor = Actor(name="Test Actor", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
    response = client.get('/actors')
    assert response.status_code == 200
    assert response.json['success'] is True
    assert len(response.json['actors']) == 1

def test_get_actors_not_found(client):
    response = client.get('/actors')
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'No actors found!' in response.json['message']

# Tests for /actors/<int:actor_id> endpoint
def test_get_actor_success(client):
    with app.app_context():
        actor = Actor(name="Test Actor", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
        actor_id = actor.id  # Access the ID while the session is active
    response = client.get(f'/actors/{actor_id}')
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['actor']['name'] == "Test Actor"

def test_get_actor_not_found(client):
    response = client.get('/actors/1')
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'Actor not found with the provided ID.' in response.json['message']

# Tests for /actors POST endpoint
def test_create_actor_success(client):
    response = client.post('/actors', json={'name': 'New Actor', 'age': 30, 'gender': 'Male'})
    assert response.status_code == 201
    assert response.json['success'] is True
    assert response.json['actor']['name'] == 'New Actor'

def test_create_actor_invalid_input(client):
    response = client.post('/actors', json={'name': 'New Actor', 'age': 30})
    assert response.status_code == 400
    assert response.json['success'] is False
    assert 'Missing required fields' in response.json['message']

# Tests for /actors/<int:actor_id> PUT endpoint
def test_update_actor_success(client):
    with app.app_context():
        actor = Actor(name="Old Name", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
        actor_id = actor.id  # Access the ID while the session is active
    response = client.put(f'/actors/{actor_id}', json={'name': 'Updated Name', 'age': 35, 'gender': 'Male'})
    assert response.status_code == 201
    assert response.json['success'] is True
    assert response.json['actor']['name'] == 'Updated Name'

def test_update_actor_not_found(client):
    response = client.put('/actors/1', json={'name': 'Updated Name', 'age': 35, 'gender': 'Male'})
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'Actor not found with the provided ID.' in response.json['message']

# Tests for /actors/<int:actor_id> DELETE endpoint
def test_delete_actor_success(client):
    with app.app_context():
        actor = Actor(name="Test Actor", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
        actor_id = actor.id  # Access the ID while the session is active
    response = client.delete(f'/actors/{actor_id}')
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'Actor deleted successfully!' in response.json['message']

def test_delete_actor_not_found(client):
    response = client.delete('/actors/1')
    assert response.status_code == 404
    assert response.json['success'] is False
    assert 'Actor not found with the provided ID.' in response.json['message']