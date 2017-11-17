from flask import Flask, render_template, redirect, url_for, session, Response
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

from bson import json_util

import User
import Story

import uuid

thread = None
thread_lock = Lock()

storyList = {}
poolMoney = 0
timer = 10
users = []
numUsers = 0


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/setTimer", methods = ["POST"])
def setTimer():
    data = request.get_json()
    try:
        time = int(data.get('time'))
    except:
        return Response(500)

    global timer

    timer = time
    print(timer)
    socketio.emit("timerUpdate", timer)

    return Response(200)

@app.route("/logout")
def logout():
    session.clear()
    return Response(200)


def timerHelper():
    global timer
    while timer > 0:
        timer-=1
        socketio.emit("timerUpdate", timer)
        socketio.sleep(1)
        if timer==1:
            winner = calculateWinner()
            socketio.emit("winner", winner)
            timer = 10
            socketio.emit("timerUpdate", timer)
            socketio.emit('updateStories', [])

@app.route("/stories")
def getStories():
    #if session.get('user') is None or session.get('user') not in users.keys():
     #   return redirect(url_for("index"))
    #session.clear()
    #print session.get('user')
    global numUsers
    global users
    if session.get('user') is None:
        userID = uuid.uuid1()
        session['user'] = userID


        users.append(userID)
        numUsers+=1

        socketio.emit("newUser", numUsers)
    elif session.get('user') not in users:

        users.append(session.get('user'))

        numUsers+=1

        socketio.emit("newUser", numUsers)

    return render_template('stories.html', uID = session.get('user'))

@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/addUser", methods=['POST'])
def addUser():
    username = request.get_json()
    global users
    if username["uname"] in users.keys():
        return Response(500)
    global poolMoney
    poolMoney += 5
    socketio.emit("updatedMoney", poolMoney)

    #adding user to state
    tempUser = User.User(username['fname'], username['lname'], username['uname'], username['pass'])
    users[tempUser.getUname()] = tempUser
    session['user'] = username["uname"]

    socketio.emit("newUser", tempUser.getName())
    #return Response(status=200)
    return url_for("getStories")

@app.route("/login", methods = ['POST'])
def login():
    username = request.get_json()
    uname = username["uname"]
    pwd = username["pass"]
    global users
    if username in users.keys():
        if users[username].getPassword() == pwd:
            session['user'] = username
            return url_for("getStories")
    return Response(401)


@socketio.on('connect')
def connect():
    print("CONNECTEDD")
    global poolMoney
    global storyList
    global numUsers
    newStories = [x.__dict__ for x in list(storyList.values())]
    emit("updatedMoney", poolMoney)
    global timer
    emit("timerUpdate", timer)
    emit('updateStories', list(reversed(newStories)))
    #allUsers = [x.getName() for x in users.values()]
    #socketio.emit("newUser", allUsers)

    socketio.emit("newUser", numUsers)

    global thread
    with thread_lock:
        if thread is None:
         	thread = socketio.start_background_task(target=timerHelper)

    # if stories =={}:
    #     temp = User.User("Zeeshan", "Hanif", "zh278", "unbanked")
    #     users[temp.getID()] = temp
    #     tempS = Story.Story("College books", temp.getID(), "I need to buy books for college", "https://cdn.eso.org/images/thumb700x/eso1238a.jpg")
    #     stories[temp.getID()] = tempS

@socketio.on('myEvent')
def handle_my_custom_event():
    print("New user connected!")


@socketio.on('addStory')
def connect(data):
    #stories.append(data)
    if data["ownerID"] not in users:
    	return
    storyList[data["ownerID"]]=(Story.Story(data["storyName"], data["ownerID"], data["storyText"], data["storyImage"]))
    newStories = [x.__dict__ for x in list(storyList.values())]
    socketio.emit('updateStories', list(reversed(newStories)))


@socketio.on('newVote')
def newVote(uID, voterID):
    #print uID, voterID
    story = storyList[uID]
    story.addUpvote(voterID)
    newStories = [x.__dict__ for x in list(storyList.values())]
    socketio.emit('updateStories', list(reversed(newStories)))



def calculateWinner():
	if len(storyList)==0 or len(users)==0:
		return "No one "
	winStory= reduce(lambda x, y : x if x.getUpvoteNum() > y.getUpvoteNum() else y, list(storyList.values()))
	#winUser = users[winStory.ownerID]
	return winStory.ownerID

def readStories():
    f = open("stories.csv")
    strs = f.readlines()
    global poolMoney
    for i, stry in enumerate(strs[1:]):
        temp = stry.split(",")
        if temp[0]=="":
            break
        poolMoney+=5
        storyList[temp[0]] = (Story.Story(temp[2], temp[0], temp[0], temp[3]))
        print temp[3]
        #print temp
    return

readStories()

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
