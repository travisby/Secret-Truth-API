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

    def assert201(self, response):
        self.assertStatus(response, 201)


class TestEndPoints(BaseTest):
    ENDPOINT = '/secret'
    SECRET = dict(secret='My Secret')

    def test_get(self):
        response = self.client.get(self.ENDPOINT)
        self.assert200(response)

    def test_post(self):
        response = self.client.post(self.ENDPOINT, data=self.SECRET)
        self.assert201(response)
