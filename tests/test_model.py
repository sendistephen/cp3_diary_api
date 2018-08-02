from app.models import User, Entry
from tests.base import BaseTestCase


class TestModelsTestcase(BaseTestCase):
    def test_create_user(self):
        user = User(user_id=1,
                    username='Sendi',
                    email='sendi.stev@gmail.com',
                    password='password')
        self.assertEqual(user.username, 'Sendi')

    def test_create_entry(self):
        entry = Entry(entry_id=1, user_id=1,
                      title='I love dancing',
                      notes='I want to learn dance lessons')
        self.assertEqual(entry.title, 'I love dancing')
