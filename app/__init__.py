# app/__init.py

from flask_restplus import Api
from flask import Blueprint, url_for
import os

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.greeting_controller import api as greeting_ns

blueprint = Blueprint('api', __name__)

if os.environ.get('HEROKU'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

    Api.specs_url= specs_url

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER_PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service')

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(greeting_ns)
