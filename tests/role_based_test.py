import unittest
from app import app, db, Movie, Actor
from flask import jsonify
from dotenv import load_dotenv
import os

"""Role Based Access Control Test Cases"""

# Access environment variables
executive_producer_key = os.getenv("EXECUTIVE_PRODUCER_KEY")
casting_director_key = os.getenv("CASTING_DIRECTOR_KEY")
casting_assistant_key = os.getenv("CASTING_ASSISTANT_KEY")

# Configure Headers based on the role
def config_header(key):
    return {
        'Authorization': f'Bearer {key}'
    }

class TestRoleBasedAccessControl(unittest.TestCase):

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
        db.session.query(Actor).delete()
        db.session.query(Movie).delete()
        db.session.commit()

    def tearDown(self):
        self.app_context.pop()

    # TODO : Need to organize the test cases in a better way

    # Casting Assistant Tests
    def test_casting_assistant_can_view_actors(self):
        response = self.client.get('/actors', headers=config_header(casting_assistant_key))
        self.assertEqual(response.status_code, 200)

    def test_casting_assistant_cannot_add_actor(self):
        response = self.client.post('/actors', json={'name': 'Actor', 'age': 30, 'gender': 'Male'}, headers=config_header(casting_assistant_key))
        self.assertEqual(response.status_code, 403)

    # Casting Director Tests
    def test_casting_director_can_add_actor(self):
        response = self.client.post('/actors', json={'name': 'Actor', 'age': 30, 'gender': 'Male'}, headers=config_header(casting_director_key))
        self.assertEqual(response.status_code, 201)

    def test_casting_director_cannot_delete_movie(self):
        response = self.client.delete('/movies/1', headers=config_header(casting_director_key))
        self.assertEqual(response.status_code, 403)

    # Executive Producer Tests
    def test_executive_producer_can_add_movie(self):
        response = self.client.post('/movies', json={'title': 'Movie', 'release_date': '2023-01-01'}, headers=config_header(executive_producer_key))
        self.assertEqual(response.status_code, 201)

    def test_executive_producer_can_delete_movie(self):
        self.client.post('/movies', json={'title': 'Movie', 'release_date': '2023-01-01'},headers=config_header(executive_producer_key))
        response = self.client.delete('/movies/1', headers=config_header(executive_producer_key))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()