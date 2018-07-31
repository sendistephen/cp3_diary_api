from pprint import pprint
from urllib.parse import urlparse

import psycopg2


class Connection:
    """Method handles database connection"""

    def __init__(self, database_url):
        # try:
        parsed_url = urlparse(database_url)
        dbname = parsed_url.path[1:]
        user = parsed_url.username
        host = parsed_url.hostname
        password = parsed_url.password
        port = parsed_url.port
        
        self.connection = psycopg2.connect(
            database=dbname, user=user, password=password, host=host, port=port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        pprint("Connection successfull")
        # except:
        #     pprint("Connection to db has failed.")

    def create_tables(self):
        """This method handles creation of database tables"""
        query_table_user = "CREATE TABLE IF NOT EXISTS\
        users(user_id SERIAL PRIMARY KEY ,username text, email text, password text)"
        self.cursor.execute(query_table_user)

        self.connection.commit()
        self.connection.close()

    def trancate_table(self, table):
        """Trancates the table"""
        self.cursor.execute(
            "TRUNCATE TABLE {} RESTART IDENTITY cascade ".format(table))
