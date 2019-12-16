import uuid
import datetime

from app.main import db
from app.main.model.user import User

"""All the logic components and querys"""


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def delete_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if user:
        delete_entry(user)
        response_object = {
            'status': 'success',
            'message': 'User successfully deleted.',
        }
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'User not found.',
        }
        return response_object


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def delete_entry(user):
    db.session.delete(user)
    db.session.commit()


def save_changes(user):
    db.session.add(user)
    db.session.commit()
