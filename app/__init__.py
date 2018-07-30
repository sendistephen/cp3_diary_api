from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dbconnection import Connection

from config import app_config
from app.views import RegisterResource


def create_app(config_name):
    """This function is the application factory"""

    # instantiate flask app
    my_app = Flask(__name__, instance_relative_config=True)
    my_app.config.from_object(app_config[config_name])

    api = Api(my_app)

    my_app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(my_app)

    connection = Connection()
    connection.create_tables()

    api.add_resource(RegisterResource, '/api/v2/auth/register')
    return my_app
