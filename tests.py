from flask import Flask as Flask
from flask.ext.testing import TestCase as FlaskTestCase


class BaseTest(FlaskTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_app(self):
        app = Flask('secret_truth')
        app.config['TESTING'] = True
        return app
