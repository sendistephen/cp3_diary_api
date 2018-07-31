import json
import unittest
from app import create_app, app_config

from dbconnection import Connection


class BaseTestCase(unittest.TestCase):
    """Handles basic configurations for unit tests"""

    def setUp(self):
        """Runs its code before every single test"""
        self.app = create_app('testing')
        # Initialize the test client
        self.client = self.app.test_client(self)
        db = Connection('postgres://admin:admin@localhost:5432/test_db')
        db.create_tables()

    def tearDown(self):
        """Drop any stored data in the list after every single test runs"""
        db = Connection('postgres://admin:admin@localhost:5432/test_db')
        db.trancate_table("users")
        db.trancate_table("entries")

    # ------------------------Register User--------------------------------#

    def register_user(self, username, email, password):
        """This methods registers the user"""
        return self.client.post(
            'api/v2/auth/register',
            data=json.dumps(dict(
                username=username,
                email=email,
                password=password
            )), content_type='application/json')

    def login_user(self, email, password):
        return self.client.post(
            'api/v2/auth/login',
            data=json.dumps(dict(
                email=email,
                password=password
            )), content_type='application/json')

 # ------------------------Create Entry--------------------------------#
    def create_entry(self, title, notes):
        return self.client.post(
            'api/v2/entries',
            data=json.dumps(dict(
                title=title,
                notes=notes
            )), content_type='application/json', headers=self.generate_token())

    def generate_token(self):
        self.register_user('katikiro', 'sendi@gmail.com', 'password')
        response = self.login_user("sendi@gmail.com", "password")
        result = json.loads(response.data.decode())

        token = result['access_token']
        authorization = {'Authorization': 'Bearer {}'.format(token)}
        return authorization
