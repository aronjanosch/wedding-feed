from app.main import jwt

from app.main.model.user import User
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity
    )
from ..service.blacklist_service import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token, prune_database
    )


class Auth:

    @staticmethod
    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decode_token):
        return is_token_revoked(decode_token)

    @staticmethod
    def login(data):
        prune_database()
        user = User.query.filter_by(email=data.get('email')).first()
        if user and user.check_password(data.get('password')):
            access_token = create_access_token(identity=data.get('email'))
            refresh_token = create_refresh_token(identity=data.get('email'))
            add_token_to_database(access_token)
            add_token_to_database(refresh_token)
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response_object, 200
        elif user:
            response_object = {
                'status': 'fail',
                'message': 'Wrong password',
            }
            return response_object, 409
        else:
            response_object = {
                'status': 'fail',
                'message': 'User doesnt exists. Please register first.',
            }
            return response_object, 409



    @staticmethod
    def refresh():
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        add_token_to_database(access_token, get_jwt_identity())
        response_object = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'access_token': access_token,
        }
        return response_object, 200

    @staticmethod
    def get_tokens():
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        ret = [token.to_dict() for token in all_tokens]
        return ret, 200

    @staticmethod
    def modify_token(token, data):
        if not data:
            return {
                       'status': 'fail',
                       'message': 'Missing data'
                   }, 400
        revoke = data.get('revoke', None)
        if revoke is None:
            return {
                       'status': 'fail',
                       'message': "Missing 'revoke' in body"
                   }, 400
        if revoke != "True":
            return {
                       'status': 'fail',
                       'message': "'revoke' in body must be boolean"
                   }, 400

        user_identity = get_jwt_identity()
        token = token.replace('Bearer ', '')
        if revoke:
            return revoke_token(token, user_identity)
        else:
            return unrevoke_token(token, user_identity)
