from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import app_config
from app.views import RegisterResource


def create_app(config_name):
    """This function is the application factory"""

    # instantiate flask app
    my_app = Flask(__name__, instance_relative_config=True)
    my_app.config.from_object(app_config[config_name])

    return my_app


app = create_app(config_name='development')
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

# import config settings into the application
app.config.from_object(app_config['development'])

api.add_resource(RegisterResource, '/api/v2/auth/register')
