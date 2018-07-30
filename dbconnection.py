from pprint import pprint

import psycopg2


class Connection:
    """Method handles database connection"""

    def __init__(self):
        # try:
        self.connection = psycopg2.connect(
            "dbname = diary_db user=admin password=admin host=localhost port=5432")
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
