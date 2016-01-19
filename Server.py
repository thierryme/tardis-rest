#!/usr/bin/python

import serial
import json
import time

from threading import Thread, Lock

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

c = {'obstacles': [0, 0],'new_pos':[0,0,0],'mesured_pos':[0,0,0], 'nb_spots':0}
mutex = Lock()

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
        mutex.acquire()
        c[channel_name] = request.json[channel_name]
        mutex.release()
        return jsonify({channel_name: c[channel_name]}), 200


class SerialManager(Thread):
    """Communication trough serial port"""
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)#pour killer le thread avec ctrl + C

    def run(self):
        ser_connected = "No serial"
        #dat = c['new_pos']
        #print dat
        #print "dans le thread"
        while True:
            #dat = c['new_pos']
            #print dat
            try:
                ser = serial.Serial('/dev/ttyUSB1', 115200)  # open serial port
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

	                    data_to_send = {}
	                    data_to_send['new_pos'] = [200, 200, 0]
	                    data_to_send['new_pos'] = c['new_pos']
	                    #print dat

	                    ser.write(json.dumps(data_to_send)+'\n')
                finally:
	                ser.close()
	                print("{} disconnected".format(ser_connected))
            except serial.serialutil.SerialException:
                time.sleep(3)
                print "dans le thread"


if __name__ == '__main__':

    serialManager = SerialManager()
    serialManager.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
