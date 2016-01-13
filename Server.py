#!/usr/bin/python2.7
from flask import Flask,request

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

c = {'obstacles':[2,3]}
@app.route('/channels')
@app.route('/channels/<channel_name>',methods=['GET','POST'])
def f(channel_name=None):
	if request.method == 'GET':

	    if channel_name == None:
	        #print all channels
	        for val in c.iteritems():
	            return "{}".format(val)
	    else:
	        return "{}".format(c[channel_name])
	#si methode POST
	else:
		if not request.json:
			abort(400)
		c[channel_name] = request.json[channel_name]
		return "{}".format(c)

#@app.route('/channels/<channel_name>',methods=['POST'])
#def postDico(channel_name):


if __name__ == '__main__':
    app.run(port=5000, debug=True)