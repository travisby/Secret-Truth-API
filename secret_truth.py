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
            message = queue.get()['messages'].pop()
            queue.delete(message['id'])
            return jsonify(secret=message['body'])

    return app

if __name__ == '__main__':
    create_app().run()
