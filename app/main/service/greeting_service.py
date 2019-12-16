import uuid
import datetime

from app.main import db
from app.main.model.greeting import Greeting

"""All the logic components and querys"""


def save_new_greeting(data):
    new_greeting = Greeting(
        author=data['author'],
        message=data['message'],
        pic=data['pic']
    )
    save_changes(new_greeting)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.',
    }
    return response_object, 201


def delete_greeting(data):
    greeting = Greeting.query.filter_by(id=data['id']).first()
    if greeting:
        delete_entry(greeting)
        response_object = {
            'status': 'success',
            'message': 'Greeting successfully deleted.',
        }
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Greeting not found.',
        }
        return response_object


def get_all_greetings():
    return Greeting.query.all()


def get_a_greeting(public_id):
    return Greeting.query.filter_by(id=public_id).first()


def delete_entry(greeting):
    db.session.delete(greeting)
    db.session.commit()


def save_changes(greeting):
    db.session.add(greeting)
    db.session.commit()
