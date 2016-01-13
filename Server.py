#!/usr/bin/python2.7
import serial
from flask import Flask

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
@app.route('/channels/<channel_name>', methods=['GET'])
def f(channel_name=None):
    if channel_name is None:
        #print all channels
        for val in c.iteritems():
            return "{}".format(val)
    else:
        return "{}".format(c[channel_name])


if __name__ == '__main__':
    print("coco")

    from threading import Thread

    server = Thread(target=app.run, kwargs={'port':5000, 'debug':False, 'use_reloader':False, 'threaded':True})

    #app.run()
    server.start()
    print("coucou")

    import sys

    # def unblocking_read():
    #     """ Read user input in a non-blocking way using select """

    #     from select import select

    #     timeout = 0
    #     sys.stdout.flush()
    #     read, _, _ = select([sys.stdin], [], [], timeout)
    #     if read:
    #         return sys.stdin.readline()
    #     else:
    #         return ""

    ser = serial.Serial('/dev/ttyACM0', 9600)  # open serial port
    print(ser.name)         # check which port was really used

    # while True:
    #     data = unblocking_read()
    #     if data != "":

    #         ser.write(data)     # write a string

    #     if '\n' in data:
    #         line = ser.readline()
    #         print(line)

    while True:
        print("toto")
        line = ser.readline()
        print(line)

    ser.close()
