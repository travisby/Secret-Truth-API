from flask import Flask, json
from flask.ext.testing import TestCase as FlaskTestCase

from collections import deque

from secret_truth import create_app, FORM_FIELD


ENDPOINT = '/secret'
SECRET = dict(secret='My Secret')


class BaseTest(FlaskTestCase):

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

    def test_post_queue_adds_item(self):
        self.client.post(ENDPOINT, data=SECRET)
        self.assertEqual(self.queue.get(), SECRET[FORM_FIELD])

    def test_get_queue_returns_added_item(self):
        self.queue.post(SECRET[FORM_FIELD])
        resp = self.client.get(ENDPOINT)
        self.assertEqual(
            json.loads(resp.data)[FORM_FIELD],
            SECRET[FORM_FIELD]
        )

    def test_ensure_item_removed_after_get(self):
        self.queue.post(SECRET[FORM_FIELD])
        self.client.get(ENDPOINT)
        self.assertTrue(self.queue.empty())

    def test_add_item_to_queue_makes_size_1(self):
        self.client.post(ENDPOINT, data=SECRET)
        self.assertEqual(self.queue.size(), 1)


class MyQueue(deque):

    def get(self):
        return self.popleft()

    def post(self, item):
        self.append(item)

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self)
