from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.dto import GreetingDto
from ..service.greeting_service import save_new_greeting, get_all_greetings, get_a_greeting, delete_greeting

api = GreetingDto.api
_greeting = GreetingDto.greeting

"""Contains the endpoints of the REST API"""


@api.route('/')
class GreetingList(Resource):
    @api.doc('list_list_of_registered_greetings')
    @api.marshal_with(_greeting, envelope='data')
    @jwt_required
    def get(self):
        """List all registered greetings"""
        return get_all_greetings()

    @api.response(201, 'Greeting successfully created')
    @api.doc('create a new greeting')
    @api.expect(_greeting, validate=True)
    def post(self):
        """Creates a new Greeting"""
        data = request.json
        return save_new_greeting(data=data)

    @api.response(200, 'Greeting successfully deleted')
    @api.doc('delete a greeting')
    @api.expect(_greeting, validate=True)
    @jwt_required
    def delete(self):
        """Deletes a Greeting"""
        data = request.json
        return delete_greeting(data=data)

@api.route('/<greeting>')
@api.param('greeting', 'The greeting identifier')
@api.response(404, 'Greeting not found')
class Greeting(Resource):
    @api.doc('get a greeting')
    @api.marshal_with(_greeting)
    def get(self, greeting):
        """get a greeting given by its identifier"""
        greeting = get_a_greeting(greeting)
        if greeting:
            return greeting
        else:
            api.abort(404)
