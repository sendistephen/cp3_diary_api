import os
# from config import app_config
from app import create_app
from dbconnection import Connection

APP = create_app()


if __name__ == '__main__':
    connection = Connection('postgresql://localhost/test_db')
    connection.create_tables()
    APP.run(debug=True)
