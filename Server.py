#!/usr/bin/python

import serial
import json

from threading import Thread

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# @app.route('/')
# @app.route('/<chemin>')
# def index(chemin=None):
#     return "Hello {}!".format(chemin)
# @app.route('/channels/obstacles')
# def obstacle():
#     pass
# @app.route('/channels/newpos/<x><y><teta>')#rajoute methode post
# def newpos(x,y,teta):
#     pass
# @app.route('/channels/mesuredpos')
# def mesuredpos():
#     pass

c = {'obstacles': [2, 3]}


@app.route('/channels')
@app.route('/channels/<channel_name>', methods=['GET', 'POST'])
def f(channel_name=None):
    if request.method == 'GET':
        if channel_name is None:
            #print all channels
            return jsonify(c)

        else:
            return jsonify({channel_name: c[channel_name]})

    #si methode POST
    else:
        if not request.json:
            abort(400)
        c[channel_name] = request.json[channel_name]
        return jsonify({channel_name: c[channel_name]}), 200


class SerialManager(Thread):
    """Communication trough serial port"""
    def __init__(self):
        super(SerialManager, self).__init__()

    def run(self):
        ser = serial.Serial('/dev/ttyACM0', 9600)  # open serial port
        print(ser.name)         # check which port was really used

        while True:
            line = ser.readline()
            try:
                data = json.loads(line)
                print(data)
            except ValueError:
                print("Non-valid")

        ser.close()

if __name__ == '__main__':

    serialManager = SerialManager()

    serialManager.run()
    app.run(port=5000)

    serialManager.join()
