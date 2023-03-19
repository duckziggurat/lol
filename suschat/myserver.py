from multiprocessing.util import log_to_stderr
from operator import le
from flask import Flask, request, render_template, copy_current_request_context
import json
import traceback
from flask_socketio import SocketIO, emit
import banana_dev as banana
import re
import logging
import random
import threading
import os
import time
import asyncio

# import gevent
import aiohttp
import os
from multiprocessing import Process

app = Flask(__name__)
socket = SocketIO(app)


@app.route("/")
def index():

    return render_template("client.html")


# 3600 characters
model_key = "gptj"
unavailable_names = list()
chatbots = list()
bot_names = list()
avail_names = ["bot1", "bot2", "bot3", "bot4", "bot5", "bot6"]




class Chatbot:
    def __init__(self):
        random_name = random.choice(avail_names)
        avail_names.remove(random_name)
        self.name = random_name
        print("actual name:" + self.name)



@socket.on("connect")
def connect(parameter):
    if not chatbots:
        randomnum = random.randint(1, 6)

        for n in range(randomnum):
            chatbots.append(Chatbot())
            print("bot " + str(n) + " created")
    print(len(chatbots))
    print("[CLIENT CONNECTED]:", request.sid)


@socket.on("disconnect")
def disconn():
    print("[CLIENT DISCONNECTED]:", request.sid)


@socket.on("notify")
def notify(user):
    emit("notify", user, broadcast=True, skip_sid=request.sid)


@socket.on("data")
def emitback(data):
    print(data["message"])
    json_data = json.dumps(data)
    emit("returndata", json_data, broadcast=True)




@socket.on("bot_write_data")
def handle_bot_write_data():
    print("hi")
    chatbot_name = random.choice(chatbots).name
    message = f"[{chatbot_name}]: Hello"
 

    emit("returnchatbotdata", message, broadcast=True)




if __name__ == "__main__":
    socket.run(app)
