from flask import Flask, render_template
import socketio
import eventlet
import eventlet.wsgi
from flask_socketio import SocketIO
import json

from flask_socketio import send, emit
from threading import Thread
from time import sleep
import random

stories = []

#sio = socketio.AsyncServer(async_mode='aiohttp')
#app = Flask(__name__)
#sio.attach(app)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

stories = []
poolMoney = 0

@app.route("/")
def hello():
    return render_template('stories.html')

@app.route("/main")
def main():
	return render_template('main.html')

@app.route("/index")
def index():
	return render_template('index.html')

@socketio.on('connect')
def connect():
    print("CONNECTEDD")
    emit("updatedMoney", poolMoney)

@socketio.on('myEvent')
def handle_my_custom_event():
    print("New user connected!")


@socketio.on('addStory')
def connect(data):
    stories.append(data)
    print("New story", data)
    socketio.emit('updateStories', stories)

@socketio.on('newVote')
def newVote(data):
    print("New vote", data)
    # socketio.emit('updateStories', stories)

@socketio.on('addUser')
def connect(data):
    print("Username joined:", username)
    userBal = random.randint(100,1000)
    poolMoney += userBal
    emit("updatedMoney", poolMoney)


def calculateWinner():
	return "Lixuan"

def countdown(t, *fun):
    import time
    print('This window will remain open for 3 more seconds...')
    while t >= 0:
        print(t)
        time.sleep(1)
        t -= 1
    print('Goodbye! \n \n \n \n \n')
    fun()
    

#thread = Thread(target = countdown, args = (5, ))
#thread.start()
#thread.join()
#emit("gotWinner", calculateWinner())




if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    # app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    # eventlet.wsgi.server(eventlet.listen  p)
    socketio.run(app)


