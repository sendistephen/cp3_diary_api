from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from pytz import utc

from dbconnection import Connection
import re
from datetime import datetime
from app.models import User

connection = Connection()


class RegisterResource(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

        args = parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        email_exists = User.email_exists(email)

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({'message': 'Please enter a valid email.'}), 400)

        if username.strip() == '' or len(username.strip()) < 3:
            return make_response(jsonify({'message': 'Please enter a valid username.'}), 400)

        if password.strip() == '' or len(password.strip()) < 5:
            return make_response(jsonify({'message': 'Please enter a valid password.'}), 400)

        if not email_exists:
            User.create_user_account(username, email, password)
            return make_response(jsonify({'message': 'User successfully registered.'}), 201)

        return make_response(jsonify({'message': 'Email already taken.'}), 400)
