from flask import Flask, render_template
import socketio
import eventlet
import eventlet.wsgi

sio = socketio.Server()
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('main.html')

@sio.on('connect')
def connect(sid, environ):
    print("CONNECTEDD")

@sio.on('myEvent')
def connect():
    print("CONNECTEDD to my event")

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
