from flask import Flask, json
from flask.ext.testing import TestCase as FlaskTestCase

from uuid import uuid1

from secret_truth import create_app, FORM_FIELD


ENDPOINT = '/secret'
SECRET1 = dict(secret='My Secret')
SECRET2 = dict(secret='Bob\'s Secret')
DIRTY_SECRET = dict(secret="<script>alert('Not-Sanitized!');</script>")


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
        self.client.post(ENDPOINT, data=SECRET1)
        self.assertEqual(
            self.queue.get()['messages'].pop()['body'],
            SECRET1[FORM_FIELD]
        )

    def test_get_queue_returns_added_item(self):
        self.queue.post(SECRET1[FORM_FIELD])
        resp = self.client.get(ENDPOINT)
        self.assertEqual(
            json.loads(resp.data)[FORM_FIELD],
            SECRET1[FORM_FIELD]
        )

    def test_ensure_item_removed_after_get(self):
        self.queue.post(SECRET1[FORM_FIELD])
        self.client.get(ENDPOINT)
        self.assertTrue(self.queue.empty())

    def test_add_item_to_queue_makes_size_1(self):
        self.client.post(ENDPOINT, data=SECRET1)
        self.assertEqual(self.queue.size(), 1)

    def test_add_two_items_get_first_back(self):
        self.queue.post(SECRET1[FORM_FIELD])
        self.queue.post(SECRET2[FORM_FIELD])
        resp = self.client.get(ENDPOINT)
        self.assertEqual(
            json.loads(resp.data)[FORM_FIELD],
            SECRET1[FORM_FIELD]
        )

    def test_input_gets_sanitized(self):
        resp = self.client.post(ENDPOINT, data=DIRTY_SECRET)
        self.assertNotEqual(
            self.queue.get()['messages'].pop()['body'],
            DIRTY_SECRET[FORM_FIELD]
        )


class TestQueue(BaseTest):

    def test_ironmq_raises(self):
        app_func = lambda: create_app()
        self.assertRaises(ValueError, app_func)


class MyQueue(list):

    def get(self, max_length=1):
        return {'messages': self[:max_length]}

    def post(self, item):
        self.append({'id': '%s' % uuid1(), 'body': item})

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self)

    def delete(self, delete_id):
        item = [x for x in self if x['id'] == delete_id].pop()
        index = self.index(item)
        del(self[index])
