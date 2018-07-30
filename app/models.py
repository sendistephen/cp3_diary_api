import json
from datetime import datetime

from pytz import utc

from dbconnection import Connection

connection = Connection()


class User:
    """This class represents the user object"""

    def __init__(self, user_id, username, password, email):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

    def json(self):
        """Representation of user object in json format"""
        return json.dumps({
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        })

    @staticmethod
    def create_user_account(username, email, password):
        create_user_query = "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)"
        connection.cursor.execute(
            create_user_query, (username, email, password))

    @staticmethod
    def email_exists(email):
        select_query = "SELECT * FROM users WHERE email = %s"
        connection.cursor.execute(select_query, [email])
        row = connection.cursor.fetchone()
        return row
