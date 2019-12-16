from datetime import datetime
from flask_jwt_extended import decode_token

from app.main import db
from ..model.blacklist import BlacklistToken


def _epoch_utc_to_datetime(epoch_utc):
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token):
    """
    Adds a new token to the database
    :param encoded_token:
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token['identity']
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    db_token = BlacklistToken(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )

    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(decoded_token):
    """
    Checks if given token is revoked ir not.
    We add all tokens to db, so if its not present = revoked
    :param decoded_token:
    """
    jti = decoded_token['jti']
    token = BlacklistToken.query.filter_by(jti=jti).one()
    if token:
        return token.revoked
    else:
        return True


def get_user_tokens(user_identity):
    """
    Returns all of the tokens, revoked and unrevoked, of the given user
    :param user_identity:
    """
    return BlacklistToken.query.filter_by(user_identity=user_identity).all()


def revoke_token(encoded_token, user):
    """
    Revokes given token
    :param user:
    """
    jti_ = decode_token(encoded_token)['jti']
    token = BlacklistToken.query.filter_by(jti=jti_, user_identity=user).one()
    if token:
        token.revoked = True
        db.session.commit()
        response_object = {
                              'status': 'success',
                              'message': 'Token revoked.'.format(user),
                          }, 400
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Token from user {} not found.'.format(user),
        }, 400
        return response_object


def unrevoke_token(encoded_token, user):
    """
    Unrevokes given token.
    :param user:
    """
    jti_ = decode_token(encoded_token)['jti']
    token = BlacklistToken.query.filter_by(jti=jti_, user_identity=user).one()
    if token:
        token.revoked = False
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Token unrevoked.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Token of user {} not found.'.format(user),
        }
        return response_object, 400


def prune_database():
    """
    Delete tokens that have expired.
    :return:
    """
    now = datetime.now()
    expired = BlacklistToken.query.filter(BlacklistToken.expires < now).all()
    for token in expired:
        db.session.delete(token)
    db.session.commit()
