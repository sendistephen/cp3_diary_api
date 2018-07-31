from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from dbconnection import Connection
import re
from datetime import datetime
from pytz import utc
from app.models import User, Entry

connection = Connection('postgres://admin:admin@localhost:5432/diary_db')


class RegisterResource(Resource):
    """ Defines endpoints for method calls for a user
        methods: GET, POST
        url: /api/auth/register
        url: /api/auth/login
     """

    def post(self):
        """Handles registration of a new user"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

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


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        email_exists = User.email_exists(email)
        valid_password = User.valid_password(password)

        if email_exists and valid_password:
            access_token = create_access_token(
                identity=email_exists)
            return make_response(jsonify({
                'message': 'Congratulations. Login successfully.',
                'access_token': access_token}), 200)

        return make_response(jsonify({
            'message': 'Email or password is invalid. Enter valid credentials'}
        ), 400)


class EntryListResource(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('notes', type=str)

        args = parser.parse_args()
        title = args['title']
        notes = args['notes']

        user_id = get_jwt_identity()

        title_exists = Entry.get_entry_title(title, user_id[0])

        date_created = datetime.now(utc)

        # validate user input here
        if len(title.strip()) < 4:
              return make_response(jsonify(
            {'message': 'Please enter a valid entry.'}), 400)

        if len(notes.strip()) < 5:
              return make_response(jsonify(
            {'message': 'Please enter notes with atleast 5 characters.'}), 400)

        if not title_exists:
            Entry.create_entry(user_id[0], title, notes, str(date_created))
            return make_response(jsonify({
                'message': 'Entry recorded successfully.'}), 201)
        return make_response(jsonify(
            {'message': 'Cannot have entries with the same title.'}), 400)
