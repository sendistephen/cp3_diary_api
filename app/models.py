import json
from datetime import datetime

from pytz import utc

from dbconnection import Connection

connection = Connection('postgres://admin:admin@localhost:5432/diary_db')


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

    @staticmethod
    def find_user_by_id(user_id):
        select_user_query = "SELECT * FROM users WHERE user_id = %s"
        connection.cursor.execute(select_user_query, [user_id])
        row = connection.cursor.fetchone()
        return row

    @staticmethod
    def valid_password(password):
        select_password_query = "SELECT * FROM users WHERE password = %s"
        connection.cursor.execute(select_password_query, [password])
        row = connection.cursor.fetchone()
        return row


class Entry:
    def __init__(self, entry_id, user_id, title, notes):
        self.id = entry_id
        self.user_id = user_id
        self.title = title
        self.notes = notes
        self.date_created = datetime.now(utc)

    def json(self):
        return json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'notes': self.notes,
            'date_created': self.date_created
        })

    @staticmethod
    def create_entry(user_id, title, notes, date_created):
        query_create_entry = "INSERT INTO entries(user_id, title, notes, date_created) VALUES (%s,%s,%s,%s)"
        connection.cursor.execute(
            query_create_entry, (user_id, title, notes, date_created))

    @staticmethod
    def get_entry_title(title, user_id):
        query_select_entry = "SELECT title FROM entries WHERE title = %s AND user_id = %s"
        connection.cursor.execute(query_select_entry, [title, user_id])
        row = connection.cursor.fetchone()
        return row

    @staticmethod
    def get_all_entries(user_id):
        query_select_all_entries = "SELECT * FROM entries WHERE user_id = %s"
        connection.cursor.execute(query_select_all_entries, [user_id])
        rows = connection.cursor.fetchall()
        return [{'id': row[0], 'title':row[2], 'notes':row[3], 'date-created':row[4]} for row in rows]

    @staticmethod
    def get_user_entry_by_id(entry_id, user_id):
        query_to_get_single_entry = "SELECT * FROM entries WHERE entry_id= %s AND user_id=%s"
        connection.cursor.execute(query_to_get_single_entry, (entry_id, user_id))
        row = connection.cursor.fetchone()
        return [{'id': row[0],'title': row[2], 'notes':row[3], 'date-created':row[4]}]
