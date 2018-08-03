import json
import unittest
from app import create_app
from flask import Flask
from config import app_config
from dbconnection import Connection


class BaseTestCase(unittest.TestCase):
    """Handles basic configurations for unit tests"""

    def setUp(self):
        """Runs its code before every single test"""
        # Initialize the test client

        self.app = create_app()
        self.client = self.app.test_client()
        db = Connection('postgresql://localhost/test_db')
        db.create_tables()

    def tearDown(self):
        """Drop any stored data in the list after every single test runs"""
        db = Connection('postgresql://localhost/test_db')
        db.truncate_table("users")
        db.truncate_table("entries")

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

    def get_all_entries(self):
        return self.client.get(
            'api/v2/entries', content_type='application/json',
            headers=self.generate_token()
        )

    def update_user_entry(self):
        return self.client.put(
            'api/v2/entries/1',
            data=json.dumps(dict(
                title='Learning about OOP',
                notes='Taking a full course for 2 months'
            )), content_type='application/json', headers=self.generate_token())

    def get_single_entry(self):
        return self.client.get(
            'api/v2/entries/1',
            content_type='application/json',
            headers=self.generate_token()
        )

    def get_single_entry_with_invalid_id(self):
        return self.client.get(
            'api/v2/entries/9',
            content_type='application/json',
            headers=self.generate_token()
        )

    def generate_token(self):
        self.register_user('katikiro', 'sendi@gmail.com', 'password')
        response = self.login_user("sendi@gmail.com", "password")
        result = json.loads(response.data.decode())

        token = result['access_token']
        authorization = {'Authorization': 'Bearer {}'.format(token)}
        return authorization


if __name__ == '__main__':
    unittest.main()
