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
#import gevent
import aiohttp
import os
from multiprocessing import Process

app = Flask(__name__)
socket = SocketIO(app)
@app.route('/')
def index():
    
    return render_template('client.html')

#3600 characters
model_key = "gptj"
unavailable_names = list()
chatbots = list()
bot_names = list()
avail_names  = ["bot1", "bot2", "bot3", "bot4", "bot5", "bot6"]

#class BackgroundTasks(threading.Thread):
#    def run(self,*args,**kwargs):
#        while True:
#            gevent.spawn(random.choice(chatbots).emit_botdata())
#            if (random.randint(0,1) == 1):
#                time.sleep(random.randint(0,20)) 
#def generate_raw_text(data,text_length):
    #model_inputs = { "text": data , "length": text_length, "temperature": 0.9, "topK": 50, "topP": 0.9}
    #banana_output = banana.run(api_key,model_key,model_inputs)
    #print("hi")
    #outputs_string = json.dumps(banana_output['modelOutputs'])
    #entire_output_text = outputs_string[13:outputs_string.find('", "input":')]
    #return entire_output_text
def generate_name():
    #name = generate_raw_text("My name is",random.randint(1,20)).strip()
    #startidx = 0
    #for n in range(len(name)):
    #    if (name[n].isalpha() == True):
    #            startidx = n
    #            break
    #for n in range(startidx,len(name)):
    #    if (name[n].isalpha() == False):
    #        unavailable_names.append(name[:n])
    #        return name[:n]          
    #if name in unavailable_names:
      #  print('name in unavailable names')
     #   name = generate_name()
    
    #get first alphabetical character
   
    #for n in range(startidx,len(name)):
    #    if (name[n].isalpha() == False):
    #        print('return-name:' + name[n:])
    #        return name[:n]
    return name
class Chatbot:
    def __init__(self):
        random_name = random.choice(avail_names)
        avail_names.remove(random_name)
        self.name = random_name
        print('actual name:' + self.name)
    #def return_name(self):
    #    name = generate_name()
    #    while (name in unavailable_names):
   #         print("name in unavailable")
   #         name = generate_name()
   #     unavailable_names.add(name)
   #     return name
    #def emit_botdata(self):
    #    chatbot_output = '[' + self.name +']:' + get_chatbot_output(chat_history.get_history() + '\n' + '[' + self.name +']:')
    #    print(chatbot_output)
    #    print('chatbot name is' + self.name)
    #    emit('returnchatbotdata',chatbot_output, broadcast=True)
    
    
    
        

    



class History:
    __history_string = ""
    def get_history(self):
        return self.__history_string
    def set_history(self,chat_item):
        if (len(self.__history_string + chat_item) > 3200):
            self.__history_string = self.__history_string[len(chat_item):] + chat_item
        else:
            self.__history_string += chat_item
chat_history = History()
#def replace_subsequent_periods(str):
#    output = str
#    period_indices =[i for i, c in enumerate(str) if c == '.']
#    for n in period_indices:
#        if (n < len(str) - 1) and (str[n] == str[n + 1]):
#            output = str[:n] + "#" + str[n + 1:]
#    return output

def purge_of_starting_characters(str):
    for n in range(len(str)):
        if (str[n].isalpha() == False):
            return str[n + 1:]
    return str
def remove_escapes(input_string):
    #print("before removing escapes:" + str)
    #escapes = ''.join([chr(char) for char in range(1, 32)])
    #for esc in escapes:
    #    print(esc)
    #    str.replace(esc,"")
    #new_str = "".join(c for c in str if c not in escapes)
    #if ("".join(c for c in str if c in escapes)):
    #    print('escapes' + "".join(c for c in str if c in escapes))
    #    new_str = remove_escapes(new_str)
       
    #return str.replace("\n","")
    s = input_string.translate({key: None for key in range(1, 32)})
    return s.replace(r"\n"," ")

def get_period_indices(str):
    period_indices = [i for i, c in enumerate(str) if c == '.']
    return [i for i in period_indices if i > 10]


def remove_faux_chatlog(input_string):
    sliced_output = remove_escapes(input_string[:list(re.finditer('\[(.*?)\]',input_string))[1].start()])
    return sliced_output #+ generate_gpt_text(data + sliced_output)


def generate_gpt_text(data):
    entire_output_text = generate_raw_text(data,150)
    period_list = get_period_indices(entire_output_text)
    if (len(period_list) == 0):
        return entire_output_text
    else:
        return entire_output_text[:random.choice(period_list)]
    #return entire_output_text[:random.choice(period_list)] if (len(period_list) > 0 or len(entire_output_text) < 3000) else entire_output_text[period_list[0]]
def get_chatbot_output(data):
    chatbot_output = generate_gpt_text(data)
    print('chatbot output gotten')
    while (len(re.findall('\[(.*?)\]',chatbot_output)) > 1):
        chatbot_output = remove_faux_chatlog(chatbot_output)
    #if (re.search('\[(.*?)\]',chatbot_output)):
    #    first_faux_chatlog = re.search('\[(.*?)\]',chatbot_output).group(0)
    #    return purge_of_starting_characters(remove_escapes(chatbot_output[chatbot_output.find(first_faux_chatlog) + len(first_faux_chatlog):]))
    return chatbot_output



@socket.on('connect')
def connect(parameter):
    if not chatbots:
        randomnum = random.randint(1,6)

        for n in range(randomnum):
            chatbots.append(Chatbot())
            print('bot ' + str(n) +' created')
    print(len(chatbots))
    print("[CLIENT CONNECTED]:", request.sid)
@socket.on('disconnect')
def disconn():
    print("[CLIENT DISCONNECTED]:", request.sid)
@socket.on('notify')
def notify(user):
    #unavailable_names.add(user)
    emit('notify', user, broadcast=True, skip_sid=request.sid)
@socket.on('data')
def emitback(data):
    #chat_history.set_history(data)
    print(data['message'])
    json_data = json.dumps(data)
    emit('returndata', json_data, broadcast=True)

    #emit()
@socket.on('bot_write_data')
def handle_bot_write_data():
    print("hi")
    chatbot_name = random.choice(chatbots).name
    message = f"[{chatbot_name}]: Hello"
    #user = data;
    #myObject = {'message': message, 'user': user}

    emit('returnchatbotdata', message, broadcast=True)
#def emit_botdata():
 #   emit('text',broadcast=True)
   # chatbot_output = get_chatbot_output(chat_history.get_history())
   # if (re.search('\[(.*?)\]',chatbot_output)):
   #     first_name_in_output = re.search('\[(.*?)\]',chatbot_output).group(1)
   #     first_faux_chatlog =  re.search('\[(.*?)\]',chatbot_output).group(0)
   #     if (first_name_in_output.upper() in (name.upper() for name in bot_names)):
    #        print('contains bot name:' +purge_of_starting_characters(remove_escapes(chatbot_output)) )
    #        emit('returnchatbotdata',purge_of_starting_characters(remove_escapes(chatbot_output)),broadcast=True)
    #    else:
     #       print('contains no bot name:' +purge_of_starting_characters(remove_escapes(chatbot_output)) )
     #       emit('returnchatbotdata','[' + random.choice(bot_names) + ']:' +purge_of_starting_characters(remove_escapes(chatbot_output[chatbot_output.find(first_faux_chatlog) + len(first_faux_chatlog):])),broadcast=True)
    #else:
     #   print('contains no name:' +purge_of_starting_characters(remove_escapes(chatbot_output)) )
      #  emit('returnchatbotdata',purge_of_starting_characters(remove_escapes(chatbot_output)),broadcast=True)
    #random.choice(chatbots).emit_botdata()
    
if __name__ == "__main__":
    socket.run(app)