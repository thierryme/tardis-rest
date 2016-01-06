#!/usr/bin/python2.7
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/<chemin>')
def index(chemin=None):
    return "Hello {}!".format(chemin)

if __name__ == '__main__':
    app.run(port=5000, debug=False)