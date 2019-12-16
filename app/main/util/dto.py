from flask_restplus import Namespace, fields

"""Names spaces for the DTO, similar to Blueprint"""


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password')
    })


class GreetingDto:
    api = Namespace('greetings', description='character related operations')
    greeting = api.model('greeting', {
        'author': fields.String(required=True, description='The Author'),
        'message': fields.String(required=True, description='The Message'),
        'pic': fields.String(required=False, description='path to Image')
    })

