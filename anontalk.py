from flask import Flask, render_template, url_for, request
from datetime import timedelta, datetime
from lib import ConfParser

import json

app = Flask(__name__)

chat_buffer = []
chat_buffer_max = 50

addrs = {}

config = {}
config["anontalk"] = ConfParser.parse("anontalk")

def add_chat(msg):
    chat_buffer.append(msg)

    if len(chat_buffer) == chat_buffer_max:
        chat_buffer.pop(0)


@app.route("/favicon.ico")
def favicon():
    return redirect_to(url_for('static', filename='favicon.ico'))

@app.route("/")
def index():
    return render_template("index.html", config=config)


@app.route("/chat/send", methods=["POST"])
def chat_send():

    data = request.get_json(silent=True)
    addr = request.remote_addr

    if addr in addrs:
        if addrs[addr] < datetime.now() + timedelta(seconds = -0.1):
            add_chat([data["nick"], data["msg"]])
            addrs[addr] = datetime.now()
    else:
        add_chat([data["nick"], data["msg"]])
        addrs[addr] = datetime.now()

    return "OK"

@app.route("/chat/get")
def chat_get():

    addr = request.remote_addr

    if addr in addrs:
        if addrs[addr] < datetime.now() + timedelta(seconds = -0.1):
            addrs[addr] = datetime.now()

            data = {}
            data["buffer"] = chat_buffer
            data["users"] = len(addrs)

            return json.dumps(data)
    else:
        addrs[addr] = datetime.now()
        return json.dumps(data)

    return "OK"


if __name__ == "__main__":
    app.config["DEBUG"] = config["anontalk"]["debug"]
    app.run()
