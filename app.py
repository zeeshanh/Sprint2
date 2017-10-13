from flask import Flask, render_template
import socketio
import eventlet
import eventlet.wsgi
from flask_socketio import SocketIO
<<<<<<< HEAD
import json

# sio = socketio.AsyncServer(async_mode='aiohttp')
# app = Flask(__name__)
# sio.attach(app)
=======
from flask_socketio import send, emit

stories = []

#sio = socketio.AsyncServer(async_mode='aiohttp')
#app = Flask(__name__)
#sio.attach(app)
>>>>>>> 327400b654c899645fc87d765813ed78299b4cd7

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

stories = []


@app.route("/")
def hello():
    return render_template('stories.html')

@app.route("/main")
def main():
	return render_template('main.html')


@socketio.on('connect')
def connect():
    print("CONNECTEDD")

@socketio.on('myEvent')
def handle_my_custom_event():
    print("New user connected!")


@socketio.on('addStory')
def connect(data):
    stories.append(data)
<<<<<<< HEAD
=======
    print("New story", data)
    socketio.emit('updateStories', stories)

@socketio.on('newVote')
def newVote(data):
    print("New vote", data)
    # socketio.emit('updateStories', stories)

@socketio.on('addUser')
def connect(data):
    print("Username joined:", data)
>>>>>>> 327400b654c899645fc87d765813ed78299b4cd7

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    # app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    # eventlet.wsgi.server(eventlet.listen  p)
    socketio.run(app)
