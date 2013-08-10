from flask import Flask as Flask
from flask.ext.testing import TestCase as FlaskTestCase
import secret_truth


class BaseTest(FlaskTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_app(self):
        app = secret_truth.app
        app.config['TESTING'] = True
        return app


class TestEndPoints(BaseTest):

    def test_get(self):
        response = self.client.get('/secret')
        self.assert200(response)
