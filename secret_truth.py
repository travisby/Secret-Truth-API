from flask import Flask, request

app = Flask(__name__)


@app.route('/secret', methods=['GET', 'POST'])
def get_secret():
    return '', 201
