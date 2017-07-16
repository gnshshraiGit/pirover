"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, jsonify, request, render_template
import socketio
import eventlet 
import datetime

app = Flask(__name__)

app.secret_key = "my-secret-key"
# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app

sio = socketio.Server()


@app.route('/')
def hello():
    """Renders a sample page."""
    return render_template('index.html')

@sio.on('connect', namespace='/StreamCmdSock')
def streamCmdSock_connect(sid,environ):
    print("[connected] stream socket" , sid)

@sio.on('startstream', namespace='/StreamCmdSock')
def streamCmdSock_start(sid,data):
    sio.emit('startstream',namespace='/StreamCmdSock')

@sio.on('stopstream', namespace='/StreamCmdSock')
def streamCmdSock_stop(sid,data):
    sio.emit('stopstream',namespace='/StreamCmdSock')

@sio.on('restream', namespace='/StreamCmdSock')
def streamCmdSock_restream(sid,data):
    sio.emit('restream',namespace='/StreamCmdSock')

@sio.on('connect', namespace='/WalkCmdSock')
def walkCmdSock_connect(sid,environ):
    print("[connected] walk socket" , sid)

@sio.on('gofwd', namespace='/WalkCmdSock')
def walkCmdSock_gofwd(sid,data):
    sio.emit('gofwd', {'sid':sid}, namespace='/WalkCmdSock')

@sio.on('gobkd', namespace='/WalkCmdSock')
def walkCmdSock_gobkd(sid,data):
    sio.emit('gobkd', {'sid':sid}, namespace='/WalkCmdSock')

@sio.on('gorit', namespace='/WalkCmdSock')
def walkCmdSock_gorit(sid,data):
    sio.emit('gorit', {'sid':sid}, namespace='/WalkCmdSock')

@sio.on('golft', namespace='/WalkCmdSock')
def walkCmdSock_golft(sid,data):
    sio.emit('golft', {'sid':sid}, namespace='/WalkCmdSock')

@sio.on('stop', namespace='/WalkCmdSock')
def walkCmdSock_stop(sid,data):
    sio.emit('stop', {'sid':sid}, namespace='/WalkCmdSock')

@sio.on('estop', namespace='/WalkCmdSock')
def walkCmdSock_estop(sid,data):
    sio.emit('estop', {'sid':sid}, namespace='/WalkCmdSock')

@sio.on('status', namespace='/WalkCmdSock')
def walkCmdSock_status(sid, data):
    sio.emit('status', data, room=data['sid'], namespace='/WalkCmdSock')

@sio.on('connect', namespace='/RecorderCmdSock')
def recordCmdSock_connect(sid,environ):
    print("[connected] recording socket" , sid)

@sio.on('startrecording', namespace='/RecorderCmdSock')
def recordCmdSock_start(sid,data):
    sio.emit('startrecording', {'filename':'{}_{}'.format(sid,datetime.datetime.now().strftime("%y-%m-%d-%H-%M")),'sid':sid},namespace='/RecorderCmdSock')

@sio.on('recordingcomplete', namespace='/RecorderCmdSock')
def recordCmdSock_complete(sid,data):
    sio.emit('recordingcomplete', data, room=data['sid'], namespace='/RecorderCmdSock')

if __name__ == '__main__':
    import os
    HOST = '0.0.0.0' #os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

        #wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

        # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen((HOST, PORT)), app)
