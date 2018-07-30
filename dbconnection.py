from pprint import pprint

from psycopg2 import connect


class Connection:
    """Method handles database connection"""

    def __init__(self):
        try:
            self.connection = connect(
                "dbname = diary_db user=admin password=admin host=localhost port=5432")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            pprint("Connection successfull")
        except:
            pprint("Connection to db has failed.")


if __name__ == "__main__":
    connection = Connection()