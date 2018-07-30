from flask import Flask
from flask_restful import Api

from config import app_config


def create_app(config_name):
    """This function is the application factory"""

    # instantiate flask app
    my_app = Flask(__name__, instance_relative_config=True)
    my_app.config.from_object(app_config[config_name])

    return my_app


app = create_app(config_name='development')
api = Api(app)