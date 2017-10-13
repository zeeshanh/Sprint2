from flask import Flask, render_template
import socketio
import eventlet
import eventlet.wsgi
from flask_socketio import SocketIO

stories = []

#sio = socketio.AsyncServer(async_mode='aiohttp')
#app = Flask(__name__)
#sio.attach(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def hello():
    return render_template('main.html')

@socketio.on('connect')
def connect():
    print("New user connected!")

@socketio.on('addStory')
def connect(data):
    stories.append(data)
    print("New story", data)
    socketio.emit('updateStories', stories)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    #app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    #eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
    socketio.run(app)
