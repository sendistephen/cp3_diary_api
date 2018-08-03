from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity)
from dbconnection import Connection
import re
from datetime import datetime
from pytz import utc
from app.models import User, Entry


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
            return make_response(jsonify({
                'message': 'Please enter a valid email.'}), 400)

        if not re.match(r'^[\w.-]+$', username):
            return make_response(jsonify({
                'message': 'Invalid username.',
                'status': 400
            }), 400)

        if username.strip() == '' or len(username.strip()) < 3:
            return make_response(jsonify({
                'message': 'Please enter a valid username.',
                'status': 400
            }), 400)

        if password.strip() == '' or len(password.strip()) < 5:
            return make_response(jsonify({
                'message': 'Please enter a valid password.',
                'status': 400
            }), 400)

        if not email_exists:
            User.create_user_account(username, email, password)
            return make_response(jsonify({
                'message': 'User successfully registered.',
                'status': 201
            }), 201)

        return make_response(jsonify({
            'message': 'Email already taken.',
            'status': 400
        }), 400)


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        email_exists = User.email_exists(email)
        valid_password = User.valid_password(password)

        if email_exists and valid_password:
            access_token = create_access_token(
                identity=email_exists)
            return make_response(jsonify({
                'status': 200,
                'message': 'Congratulations. Login successfully.',
                'access_token': access_token}), 200)

        return make_response(jsonify({
            'message': 'Email or password is invalid. Enter valid credentials',
            'status': 400}
        ), 400)


class EntryListResource(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('notes', type=str, required=True)

        args = parser.parse_args()
        title = args['title']
        notes = args['notes']

        user_id = get_jwt_identity()

        title_exists = Entry.get_entry_title(title, user_id[0])

        date_created = datetime.now(utc)

        # validate user input here
        if len(title.strip()) < 4:
            return make_response(jsonify(
                {
                    'message': 'Please enter a valid entry.',
                    'status': 400}
            ), 400)

        if len(notes.strip()) < 5:
            return make_response(jsonify(
                {
                    'message': 'Please enter notes with atleast 5 characters.',
                    'status': 400}),
                400)

        if not title_exists:
            Entry.create_entry(user_id[0], title, notes, str(date_created))
            return make_response(jsonify({
                'message': 'Entry recorded successfully.'}), 201)
        return make_response(jsonify(
            {'message': 'Cannot have entries with the same title.',
             'status': 201}
        ), 400)

    @jwt_required
    def get(self):
        """Returns all user entries"""
        user_id = get_jwt_identity()

        entries = Entry.get_all_entries(user_id[0])
        if entries:
            return make_response(jsonify({'Entries': entries}), 200)
        else:
            return make_response(jsonify({
                'message': 'You dont have any entries at the moment',
                'status': 200}), 200)


class EntryResource(Resource):
    """ Defines endpoints for method calls for a entry
        methods: GET, PUT, DELETE
        url: /api/v2/entries/<entry_id>
     """

    @jwt_required
    def get(self, entry_id):
        """Returns a single users entry"""
        user_id = get_jwt_identity()
        entry = Entry.get_user_entry_by_id(entry_id, user_id[0])
        if entry:
            return make_response(jsonify({'Entry': entry}), 200)
        if entry is None:
            return make_response(jsonify({
                'message': 'Entry with that id not found',
                'status': 200},
            ), 200)

    @jwt_required
    def put(self, entry_id):
        """Handles update of a single entry"""

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('notes', type=str, required=True)

        args = parser.parse_args()
        title = args['title']
        notes = args['notes']

        user_id = get_jwt_identity()

        title_exists = Entry.get_entry_title(title, user_id[0])

        date_created = datetime.now(utc)

        # validate user input here
        if len(title.strip()) < 4:
            return make_response(jsonify(
                {
                    'message': 'Please enter a valid entry.',
                    'status': 400}
            ), 400)

        if len(notes.strip()) < 5:
            return make_response(jsonify(
                {
                    'message': 'Please enter notes with atleast 5 characters.',
                    'status': 400}),
                400)
        if not title_exists:
            update = Entry.update_user_entry(user_id[0],
                                             entry_id, title, notes)

            return make_response(jsonify({
                'message': 'Entry updated successfully.',
                'status': 201},
            ), 201)
            if not update:
                return make_response(jsonify(
                    {
                        'message': 'Entry with that id not found.',
                        'status': 400}),
                    400)

        return make_response(jsonify({
            'message': 'Entry exists already.',
            'status': 400},
        ), 400)
