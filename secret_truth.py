from flask import Flask, request

app = Flask(__name__)


@app.route('/secret', methods=['GET', 'POST'])
def get_secret():

    if request.method == 'POST':
        return '', 201

    elif request.method == 'GET':
        return 'secret truth'
