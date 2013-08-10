from flask import Flask, request, jsonify
from iron_mq import IronMQ


QUEUE_NAME = 'secret'
FORM_FIELD = 'secret'


def create_app(queue=None):

    if queue is None:
        queue = IronMQ().queue(QUEUE_NAME)

    app = Flask(__name__)

    @app.route('/secret', methods=['GET', 'POST'])
    def get_secret():

        if request.method == 'POST':
            queue.post(request.form[FORM_FIELD])
            return '', 201

        elif request.method == 'GET':
            return jsonify(secret=queue.get()['messages'].pop()['body'])

    return app
