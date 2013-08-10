from flask import Flask

app = Flask(__name__)


@app.route('/secret', methods=['GET', 'POST'])
def get_secret():
    return 'secret'
