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
    