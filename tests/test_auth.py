import json
import unittest
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):
    # @unittest.skip('checking')
    def test_user_registers_successfully(self):
        """Tests user can register successfully through the api"""
        with self.client:
            response = self.register_user(
                'Sendi', 'test@test.com', 'testpassword')
            result = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(result.get('message'),
                             'User successfully registered.')

            res = self.register_user('Stephen', 'test@test.com', 'password')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data.get('message'), 'Email already taken.')

    def test_invalid_user_email_pattern(self):
        """Tests user can not register with invalid email through the api"""
        with self.client:
            response = self.register_user(
                'sendi', 'test1@test.', 'testpassword')
            result = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(result.get('message'),
                             'Please enter a valid email.')

    def test_username_contains_whitespace(self):
        """Tests user can register with whitespaces on username"""
        with self.client:
            response = self.register_user(
                'se', 'test2@test.com', 'testpassword')
            result = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(result.get('message'),
                             'Please enter a valid username.')
