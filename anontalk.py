import socketio
import eventlet
import json
from flask import Flask, render_template
from lib import ConfParser

socket = socketio.Server()
app = Flask(__name__)

anonconf = {}
anonconf["anontalk"] = ConfParser.parse("anontalk")

user_count = 0

@app.route("/")
def index():
    return render_template("index.html", anonconf=anonconf)

@socket.on("connect")
def connect(sid, environ):
    global user_count
    user_count += 1

@socket.on("disconnect")
def disconnect(sid):
    global user_count
    user_count -= 1

@socket.on("send message")
def send_message(sid, data):
    global user_count

    if len(data["nick"]) > 0:
        data["nick"] = r"{}".format(data["nick"])

    if len(data["nick"]) > 15:
        break

    if len(data["msg"]) > 200:
        break

    data["users"] = user_count
    data["msg"] = r"{}".format(data["msg"])

    socket.emit("receive chat", data)

@socket.on("get user count")
def get_user_count(sid):
    global user_count

    data = {}
    data["users"] = user_count

    socket.emit("get user count", data, room=sid)


if __name__ == "__main__":
    app.config["DEBUG"] = anonconf["anontalk"]["debug"]
    app = socketio.Middleware(socket, app)
    eventlet.wsgi.server(eventlet.listen((anonconf["anontalk"]["ip"], int(anonconf["anontalk"]["port"]))), app)
