from flask import Flask

app = Flask(__name__)


@app.route('/secret')
def get_secret():
    return 'secret'
