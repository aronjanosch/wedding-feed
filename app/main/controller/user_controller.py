from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, delete_user

api = UserDto.api
_user = UserDto.user

"""Contains the endpoints of the REST API"""

@api.route('/')
class UserList(Resource):
    @api.doc('list_list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    @jwt_required
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    #@jwt_required
    def post(self):
        """Creates a new User"""
        data = request.json
        return save_new_user(data=data)

    @api.response(200, 'User successfully deleted')
    @api.doc('delete a user')
    @api.expect(_user, validate=True)
    @jwt_required
    def delete(self):
        """Deletes a User"""
        data = request.json
        return delete_user(data=data)

@api.route('/<public_id>')
@api.param('public_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given by its identifier"""
        user = get_a_user(public_id)
        if user:
            return user
        else:
            api.abort(404)
