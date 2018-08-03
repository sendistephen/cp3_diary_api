import json
from datetime import datetime
from pytz import utc

from dbconnection import Connection

connection = Connection('postgresql://localhost/test_db')


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
        """Method handle query that adds a user to
        the database"""

        create_user_query = "INSERT INTO users \
        (username, email, password) VALUES (%s,%s,%s)"
        connection.cursor.execute(
            create_user_query, (username, email, password))

    @staticmethod
    def email_exists(email):
        """Method handles a query that checks if a user
         with an email exists already in the database"""

        select_query = "SELECT * FROM users WHERE email = %s"
        connection.cursor.execute(select_query, [email])
        row = connection.cursor.fetchone()
        return row

    @staticmethod
    def find_user_by_id(user_id):
        """Method handles a query that retrieves a user
         based on user id"""

        select_user_query = "SELECT * FROM users WHERE user_id = %s"
        connection.cursor.execute(select_user_query, [user_id])
        row = connection.cursor.fetchone()
        return row

    @staticmethod
    def valid_password(password):
        """Method handles a query that checks if user
         password is in the database"""

        select_password_query = "SELECT * FROM users WHERE password = %s"
        connection.cursor.execute(select_password_query, [password])
        row = connection.cursor.fetchone()
        return row


class Entry:
    """This class represents the entry object"""

    def __init__(self, entry_id, user_id, title, notes):
        self.id = entry_id
        self.user_id = user_id
        self.title = title
        self.notes = notes
        self.date_created = datetime.now(utc)

    def json(self):
        """Representation of entry object in json format"""

        return json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'notes': self.notes,
            'date_created': self.date_created
        })

    @staticmethod
    def create_entry(user_id, title, notes, date_created):
        """Method handle query that adds an entry to
        the database"""

        query_create_entry = "INSERT INTO entries(user_id, title, notes,\
         date_created) VALUES (%s,%s,%s,%s)"
        connection.cursor.execute(
            query_create_entry, (user_id, title, notes, date_created))

    @staticmethod
    def get_entry_title(title, user_id):
        """Method handles query that gets user
         entry based on its title"""

        query_select_entry = "SELECT title FROM entries \
        WHERE title = %s AND user_id = %s"
        connection.cursor.execute(query_select_entry, [title, user_id])
        row = connection.cursor.fetchone()
        return row

    @staticmethod
    def get_all_entries(user_id):
        """Method handles query that retrieves all user entries"""

        query_select_all_entries = "SELECT * FROM entries WHERE user_id = %s"
        connection.cursor.execute(query_select_all_entries, [user_id])
        rows = connection.cursor.fetchall()
        return [{'id': row[0], 'title':row[2], 'notes':row[3],
                 'date-created':row[4]} for row in rows]

    @staticmethod
    def get_user_entry_by_id(entry_id, user_id):
        """Method handles query that retrieves a
        user by its id"""

        query_to_get_single_entry = "SELECT * FROM entries \
        WHERE entry_id= %s AND user_id=%s"
        connection.cursor.execute(
            query_to_get_single_entry, (entry_id, user_id))
        row = connection.cursor.fetchone()
        if not row:
            return None
        return [{'id': row[0], 'title': row[2], 'notes':row[3],
                 'date-created':row[4]}]

    @staticmethod
    def update_user_entry(user_id, entry_id, title, notes):
        """Method handles a query that updates a user entry"""

        update_query = "UPDATE entries SET title = '{}', notes = '{}' \
        WHERE entry_id='{}' AND user_id='{}'"\
            .format(title, notes, entry_id, user_id)
        row = connection.cursor.execute(update_query)
        if not row:
            return None
        return row
