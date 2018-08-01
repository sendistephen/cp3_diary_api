from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dbconnection import Connection

from config import app_config
from app.views import RegisterResource, LoginResource, EntryListResource, EntryResource


def create_app():
    app = Flask(__name__)
    app.config['JWT_ALGORITHM'] = 'HS256'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app)
    api = Api(app)

    # Register endpoints here
    api.add_resource(RegisterResource, '/api/v2/auth/register')
    api.add_resource(LoginResource, '/api/v2/auth/login')
    api.add_resource(EntryListResource, '/api/v2/entries')
    api.add_resource(EntryResource, '/api/v2/entries/<entry_id>')
    return app
