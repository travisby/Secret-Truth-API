from flask import Flask, request
from iron_mq import IronMQ


QUEUE_NAME = 'secret'


def create_app(queue=None):

    if queue == None:
        queue = IronMQ().queue(QUEUE_NAME)

    app = Flask(__name__)

    @app.route('/secret', methods=['GET', 'POST'])
    def get_secret():

        if request.method == 'POST':
            return '', 201

        elif request.method == 'GET':
            return 'secret truth'

    return app
