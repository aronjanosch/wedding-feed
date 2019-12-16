from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity

from ..util.dto import AuthDto
from app.main.service.auth_service import Auth

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login(data=post_data)


@api.route('/refresh')
class UserRefresh(Resource):
    """
    User Refresh Resource
    """
    @api.doc('user refresh')
    @jwt_refresh_token_required
    def post(self):
        return Auth.refresh()


@api.route('/token')
class UserTokens(Resource):
    """
    Get User Tokens
    """
    @api.doc('get user tokens')
    @jwt_required
    def get(self):
        return Auth.get_tokens()


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @jwt_required
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        json_data = request.get_json()
        return Auth.modify_token(token=auth_header, data=json_data)
