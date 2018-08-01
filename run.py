import os
# from config import app_config
from app import create_app
from dbconnection import Connection

APP = create_app()

# APP.config.from_object(app_config['development'])

if __name__ == '__main__':
    connection = Connection('postgres://admin:admin@localhost:5432/diary_db')
    connection.create_tables()
    APP.run(debug=True)
