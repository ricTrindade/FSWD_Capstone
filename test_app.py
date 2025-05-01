import unittest
from app import app, db, Movie, Actor

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    # Tests for /movies endpoint
    def test_get_movies_success(self):
        movie = Movie(title="Test Movie", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(len(response.json['movies']), 1)

    def test_get_movies_not_found(self):
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('No movies found!', response.json['message'])

    # Tests for /movies/<int:movie_id> endpoint
    def test_get_movie_success(self):
        movie = Movie(title="Test Movie", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id
        response = self.client.get(f'/movies/{movie_id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['movie']['title'], "Test Movie")

    def test_get_movie_not_found(self):
        response = self.client.get('/movies/1')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('Movie not found with the provided ID.', response.json['message'])

    # Tests for /movies POST endpoint
    def test_create_movie_success(self):
        response = self.client.post('/movies', json={'title': 'New Movie', 'release_date': '2023-01-01'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['movie']['title'], 'New Movie')

    def test_create_movie_invalid_input(self):
        response = self.client.post('/movies', json={'title': 'New Movie'})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json['success'])
        self.assertIn('Missing required fields', response.json['message'])

    # Tests for /movies/<int:movie_id> PUT endpoint
    def test_update_movie_success(self):
        movie = Movie(title="Old Title", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id
        response = self.client.put(f'/movies/{movie_id}', json={'title': 'Updated Title', 'release_date': '2023-01-02'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['movie']['title'], 'Updated Title')

    def test_update_movie_not_found(self):
        response = self.client.put('/movies/1', json={'title': 'Updated Title', 'release_date': '2023-01-02'})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('Movie not found with the provided ID.', response.json['message'])

    # Tests for /movies/<int:movie_id> DELETE endpoint
    def test_delete_movie_success(self):
        movie = Movie(title="Test Movie", release_date="2023-01-01")
        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id
        response = self.client.delete(f'/movies/{movie_id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertIn('Movie deleted successfully!', response.json['message'])

    def test_delete_movie_not_found(self):
        response = self.client.delete('/movies/1')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('Movie not found with the provided ID.', response.json['message'])

    # Tests for /actors endpoint
    def test_get_actors_success(self):
        actor = Actor(name="Test Actor", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
        response = self.client.get('/actors')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(len(response.json['actors']), 1)

    def test_get_actors_not_found(self):
        response = self.client.get('/actors')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('No actors found!', response.json['message'])

    # Tests for /actors/<int:actor_id> endpoint
    def test_get_actor_success(self):
        actor = Actor(name="Test Actor", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
        actor_id = actor.id
        response = self.client.get(f'/actors/{actor_id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['actor']['name'], "Test Actor")

    def test_get_actor_not_found(self):
        response = self.client.get('/actors/1')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('Actor not found with the provided ID.', response.json['message'])

    # Tests for /actors POST endpoint
    def test_create_actor_success(self):
        response = self.client.post('/actors', json={'name': 'New Actor', 'age': 30, 'gender': 'Male'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['actor']['name'], 'New Actor')

    def test_create_actor_invalid_input(self):
        response = self.client.post('/actors', json={'name': 'New Actor', 'age': 30})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json['success'])
        self.assertIn('Missing required fields', response.json['message'])

    # Tests for /actors/<int:actor_id> PUT endpoint
    def test_update_actor_success(self):
        actor = Actor(name="Old Name", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
        actor_id = actor.id
        response = self.client.put(f'/actors/{actor_id}', json={'name': 'Updated Name', 'age': 35, 'gender': 'Male'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['actor']['name'], 'Updated Name')

    def test_update_actor_not_found(self):
        response = self.client.put('/actors/1', json={'name': 'Updated Name', 'age': 35, 'gender': 'Male'})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('Actor not found with the provided ID.', response.json['message'])

    # Tests for /actors/<int:actor_id> DELETE endpoint
    def test_delete_actor_success(self):
        actor = Actor(name="Test Actor", age=30, gender="Male")
        db.session.add(actor)
        db.session.commit()
        actor_id = actor.id
        response = self.client.delete(f'/actors/{actor_id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertIn('Actor deleted successfully!', response.json['message'])

    def test_delete_actor_not_found(self):
        response = self.client.delete('/actors/1')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertIn('Actor not found with the provided ID.', response.json['message'])

if __name__ == '__main__':
    unittest.main()