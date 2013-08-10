from flask import Flask as Flask
from flask.ext.testing import TestCase as FlaskTestCase

from collections import deque

from secret_truth import create_app, FORM_FIELD


class BaseTest(FlaskTestCase):
    ENDPOINT = '/secret'
    SECRET = dict(secret='My Secret')

    queue = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_app(self):
        self.queue = MyQueue()
        app = create_app(self.queue)
        app.config['TESTING'] = True
        return app

    def assert201(self, response):
        self.assertStatus(response, 201)


class TestEndPoints(BaseTest):

    def test_get(self):
        response = self.client.get(self.ENDPOINT)
        self.assert200(response)

    def test_post(self):
        response = self.client.post(self.ENDPOINT, data=self.SECRET)
        self.assert201(response)

    def test_post_queue_adds_item(self):
        self.client.post(self.ENDPOINT, data=self.SECRET)
        self.assertEqual(self.queue.get(), self.SECRET[FORM_FIELD])


class MyQueue(deque):

    def get(self):
        return self.popleft()

    def post(self, item):
        self.append(item)
