import json
import unittest
from tests.base import BaseTestCase


class EntriesTestCase(BaseTestCase):

    # @unittest.skip('checking')
    def test_user_creates_entry_successfully(self):
        with self.client:
            self.login_user("test@test.com", "password")
            response = self.create_entry(
                'Meeting with the CEO Twitter',
                'Discuss about new marketing strategies')
            result = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(result.get('message'),
                             'Entry recorded successfully.')

            res = self.create_entry(
                'Meeting with the CEO Andela',
                'Discuss about security issues'
            )
            result1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual(result1.get(
                'message'), 'Cannot have entries with the same title.')

    def test_entry_title_is_black(self):
        with self.client:
            self.login_user("test@test.com", "password")
            response = self.create_entry(
                '',
                'Discuss about new marketing strategies')
            result = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(result.get('message'),
                             'Please enter a valid entry.')
