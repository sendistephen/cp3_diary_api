import json
import unittest
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):
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
