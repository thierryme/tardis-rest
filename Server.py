#!/usr/bin/python

import serial
import json
import time
import traceback

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

channels = {'obstacles': [0, 0], 'new_pos': [0, 0, 0], 'mesured_pos': [0, 0, 0], 'nb_spots': 0}
mutex = Lock()


@app.route('/')
def client():
    return render_template('client.html')


@app.route('/channels')
@app.route('/channels/<channel_name>', methods=['GET', 'POST'])
def f(channel_name=None):
    """

    """
    if request.method == 'GET':
        if channel_name is None:
            #print all channels
            return jsonify(channels)

        else:
            return jsonify({channel_name: channels[channel_name]})

    #si methode POST
    else:
        if not request.json:
            abort(400)

        with mutex:
            channels[channel_name] = request.json[channel_name]

        return jsonify({channel_name: channels[channel_name]}), 200


class SerialManager(Thread):
    """Communication trough serial port"""
    def __init__(self, serial='/dev/ttyUSB1', baud=115200, write_c=[], read_c=[], debug=False):
        Thread.__init__(self)

        self.serial_name = serial
        self.baud = baud
        self.channels_to_write = write_c
        self.channels_to_read = read_c
        self.setDaemon(True)  # pour killer le thread avec ctrl + C
        self.debug = debug
        print('I')

    def run(self):
        ser_connected = "No serial"
        #dat = channels['new_pos']
        #print dat
        #print "dans le thread"
        while True:
            #dat = channels['new_pos']
            #print dat
            try:
                ser = serial.Serial(self.serial_name, self.baud)  # open serial port
                ser_connected = ser.name
                print("{} connected".format(ser_connected))         # check which port was really used
                #print('C')
                try:
                    while True:
                        #print('R')
                        line = ser.readline().decode('ascii')
                        if self.debug:
                            print(line)

                        try:
                            data = json.loads(line)
                            if isinstance(data, dict):
                                for key in self.channels_to_read:
                                    if key in data:
                                        with mutex:
                                            channels[key] = data[key]

                        except ValueError:
                            print("Non-valid")

                        data_to_send = {}
                        #data_to_send['new_pos'] = [200, 200, 0]

                        for channel in self.channels_to_write:
                            with mutex:
                                data_to_send[channel] = channels[channel]

                        #print('W')
                        if data_to_send != {}:
                            ser.write(json.dumps(data_to_send).encode('ascii')+'\n')

                finally:
                    ser.close()
                    print("{} disconnected".format(ser_connected))
            except serial.serialutil.SerialException:
                #traceback.print_exc()
                time.sleep(1)
                print("try reconnect")


if __name__ == '__main__':

    commDisplacingModule = SerialManager('/dev/ttyACM0006', 115200, write_c=['new_pos'], read_c=['mesured_pos'])
    commDisplacingModule.start()
    #comm2 = SerialManager('/dev/ttyUSB1', 115200, write_c=['new_pos'], read_c=['mesured_pos'])
    #comm2.start()
    commUltrasonic = SerialManager('/dev/ttyACM0004', 115200, read_c=['ultrasonic', 'avoid_direction'])
    commUltrasonic.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
