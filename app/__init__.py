from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dbconnection import Connection

from config import app_config
from app.views import RegisterResource, LoginResource, EntryListResource, EntryResource


def create_app(config_name):
    """This function is the application factory"""

    # instantiate flask app
    my_app = Flask(__name__, instance_relative_config=True)
    my_app.config.from_object(app_config['development'])

    api = Api(my_app)

    my_app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(my_app)

    connection = Connection('postgres://admin:admin@localhost:5432/diary_db')
    connection.create_tables()

    api.add_resource(RegisterResource, '/api/v2/auth/register')
    api.add_resource(LoginResource, '/api/v2/auth/login')
    api.add_resource(EntryListResource, '/api/v2/entries')
    api.add_resource(EntryResource, '/api/v2/entries/<entry_id>')
    return my_app
