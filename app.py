from flask import Flask, render_template, redirect, url_for
import socketio
import eventlet
import eventlet.wsgi
from flask_socketio import SocketIO
import json

from flask_socketio import send, emit
from threading import Thread
from time import sleep
import random
import time
import atexit
from threading import Lock
from flask import request
from functools import reduce

import User
import Story

thread = None
thread_lock = Lock()

stories = {}
poolMoney = 0
timer = 180
users = {}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def timerHelper():
    global timer
    global stories
    while timer > 0:
        timer-=1
        socketio.emit("timerUpdate", timer)
        socketio.sleep(1)
        if timer==1:
            winner = calculateWinner()
            socketio.emit("winner", winner)
            timer = 180
            socketio.emit("timerUpdate", timer)
            stories = {}
            socketio.emit('updateStories', [])

@app.route("/<id>")
def hello(id = 0):
	return render_template('stories.html', uID = id)

@app.route("/main")
def main():
	return render_template('stories.html')

@app.route("/index")
def index():
	return render_template('index.html')

@socketio.on('connect')
def connect():
    print("CONNECTEDD")
    global poolMoney
    global stories
    newStories = [x.__dict__ for x in list(stories.values())]
    emit("updatedMoney", poolMoney)
    global timer
    emit("timerUpdate", timer)
    emit('updateStories', list(reversed(newStories)))
    allUsers = [x.getName() for x in users.values()]
    socketio.emit("newUser", allUsers)
    global thread
    with thread_lock:
        if thread is None:
        	thread = socketio.start_background_task(target=timerHelper)

    if stories =={}:
        temp = User.User(name="Zeeshan", balance = 500)
        users[temp.getID()] = temp
        tempS = Story.Story("College books", temp.getID(), "I need to buy books for college", "https://cdn.eso.org/images/thumb700x/eso1238a.jpg")
        stories[temp.getID()] = tempS

@socketio.on('myEvent')
def handle_my_custom_event():
    print("New user connected!")



@socketio.on('addStory')
def connect(data):
    #stories.append(data)
    print("New story", data)
    if data["ownerID"] not in users:
    	return
    stories[data["ownerID"]]=(Story.Story(data["storyName"], data["ownerID"], data["storyText"], data["storyImage"]))
    newStories = [x.__dict__ for x in list(stories.values())]
    socketio.emit('updateStories', list(reversed(newStories)))


@socketio.on('newVote')
def newVote(uID, voterID):
    story = stories[uID]
    story.addUpvote(voterID)
    newStories = [x.__dict__ for x in list(stories.values())]
    socketio.emit('updateStories', list(reversed(newStories)))

@socketio.on('addUser')
def connect(username):
    print("Username joined:", username)
    print (username['pass'])
    # userBal = random.randint(100,1000)
    # global poolMoney
    # poolMoney += 100
    # socketio.emit("updatedMoney", poolMoney)

    # #adding user to state
    # tempUser = User.User(name = username['val'], balance = userBal-100)
    # users[tempUser.getID()] = tempUser
    # userID = tempUser.getID()
    # emit("registered", userID)
    # print('USERS', users)
    # allUsers = [x.getName() for x in users.values()]
    # socketio.emit("newUser", allUsers)


def calculateWinner():
	if len(stories)==0 or len(users)==0:
		return "No one "
	winStory= reduce(lambda x, y : x if x.getUpvoteNum() > y.getUpvoteNum() else y, list(stories.values()))
	winUser = users[winStory.ownerID]
	return winUser.getName()

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    # app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    # eventlet.wsgi.server(eventlet.listen  p)
    socketio.run(app)
