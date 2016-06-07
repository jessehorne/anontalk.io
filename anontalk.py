from flask import Flask, render_template, url_for, request, redirect
from datetime import timedelta, datetime
from lib import ConfParser

import json

app = Flask(__name__)

chat_buffer = []
chat_buffer_max = 50
chat_max_length = 100

addrs = []

config = {}
config["anontalk"] = ConfParser.parse("anontalk")

def add_chat(msg):
    if len(msg) <= chat_max_length:
        chat_buffer.append(msg)

        if len(chat_buffer) == chat_buffer_max:
            chat_buffer.pop(0)


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

@app.route("/")
def index():
    return render_template("index.html", config=config)


@app.route("/chat/send", methods=["POST"])
def chat_send():

    data = request.get_json(silent=True)
    add_chat([data["nick"], data["msg"]])

    return "{}"

@app.route("/chat/get")
def chat_get():

    data = {}
    data["buffer"] = chat_buffer
    data["users"] = len(addrs)

    return json.dumps(data)


if __name__ == "__main__":
    app.config["DEBUG"] = config["anontalk"]["debug"]
    app.run()
