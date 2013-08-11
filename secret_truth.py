"""Secret Truth API Module

Allows the POSTing and GETing of a secret from our queue.

"""
from flask import Flask, request, jsonify, escape
from iron_mq import IronMQ


QUEUE_NAME = 'secret'
FORM_FIELD = 'secret'


def create_app(queue=None):
    """Returns our Flask app"""

    if queue is None:
        queue = IronMQ().queue(QUEUE_NAME)

    app = Flask(__name__)

    @app.route('/secret', methods=['GET', 'POST'])
    def get_secret():
        """GET or POST a secret

        POST: escape, and submit into the queuing service
        GET: Return the first message from the queue
        """

        if request.method == 'POST':
            queue.post(escape(request.form[FORM_FIELD]))
            return '', 201

        elif request.method == 'GET':
            message = queue.get()['messages'].pop()
            queue.delete(message['id'])
            return jsonify(secret=message['body'])

    return app
