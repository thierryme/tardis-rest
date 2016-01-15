#!/usr/bin/python

import serial
import json
import time

from threading import Thread

from flask import Flask, request, jsonify, abort, render_template

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

c = {'avoid_direction': [2, 3]}


@app.route('/')
def client():
    return render_template('client.html')


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
        ser_connected = "No serial"

        while True:
            try:
                ser = serial.Serial('/dev/ttyUSB00_Arduino_pJaune', 9600)  # open serial port
                ser_connected = ser.name
                print("{} connected".format(ser_connected))         # check which port was really used

                try:
                    while True:

                            line = ser.readline()
                            try:
                                data = json.loads(line)
                                print(data)
                            except ValueError:
                                print("Non-valid")
                finally:
                        ser.close()
                        print("{} disconnected".format(ser_connected))

            except serial.serialutil.SerialException:

                time.sleep(3)


if __name__ == '__main__':

    # serialManager = SerialManager()

    # serialManager.run()
    app.run(port=5000, debug=True)