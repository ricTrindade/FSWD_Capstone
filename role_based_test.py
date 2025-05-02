import unittest
from app import app, db, Movie, Actor
from flask import jsonify

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

    def tearDown(self):
        self.app_context.pop()

    # TODO : Need to organize the test cases in a better way

    # Casting Assistant Tests
    def test_casting_assistant_can_view_actors(self):
        headers = {'Authorization': 'Bearer <CASTING_ASSISTANT_TOKEN>'}
        response = self.client.get('/actors', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_casting_assistant_cannot_add_actor(self):
        headers = {'Authorization': 'Bearer <CASTING_ASSISTANT_TOKEN>'}
        response = self.client.post('/actors', json={'name': 'Actor', 'age': 30, 'gender': 'Male'}, headers=headers)
        self.assertEqual(response.status_code, 403)

    # Casting Director Tests
    def test_casting_director_can_add_actor(self):
        headers = {'Authorization': 'Bearer <CASTING_DIRECTOR_TOKEN>'}
        response = self.client.post('/actors', json={'name': 'Actor', 'age': 30, 'gender': 'Male'}, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_casting_director_cannot_delete_movie(self):
        headers = {'Authorization': 'Bearer <CASTING_DIRECTOR_TOKEN>'}
        response = self.client.delete('/movies/1', headers=headers)
        self.assertEqual(response.status_code, 403)

    # Executive Producer Tests
    def test_executive_producer_can_add_movie(self):
        headers = {'Authorization': 'Bearer <EXECUTIVE_PRODUCER_TOKEN>'}
        response = self.client.post('/movies', json={'title': 'Movie', 'release_date': '2023-01-01'}, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_executive_producer_can_delete_movie(self):
        headers = {'Authorization': 'Bearer <EXECUTIVE_PRODUCER_TOKEN>'}
        response = self.client.delete('/movies/1', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()