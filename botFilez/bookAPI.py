from flask import Flask ,jsonify,request
import threading
import requests
import subprocess
import os
import signal
import time
from werkzeug.serving import make_server
from discordCreds import desired_save_dir

app = Flask(__name__)
server = None
shutdown_event = None
@app.route('/search_download/', methods = ['POST'])
def search_download():
        book_details = request.json['book_info']
        sub_com_args = ['python3' , './bookBot.py', book_details]
        outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
        if outcome.returncode == 0:
            return "OK" , 200
        else:
            return "Nope", 204
        
@app.route('/cleanup/',methods = ['GET'])
def cleanup():
    try:
        for items in os.listdir(desired_save_dir):
            file_path = os.path.join(desired_save_dir,items)
            if os.path.isfile(file_path) and items.endswith('epub'):
                os.remove(file_path)
    except:
        print("nothing to remove")
    return "Clean up finished." , 200
    

@app.route('/shutdown/',methods = ['POST'])
def shutdown():
    shutdown_server()
    return 'Shutting down...', 200

def shutdown_server():
    global shutdown_event
    shutdown_event.set()
    time.sleep(2)

def spin_up(event):
    global server
    global shutdown_event
    shutdown_event = event
    server = make_server('127.0.0.1',5000,app)
    server.serve_forever()

if __name__ == '__main__':
    print("API spun up.")
    spin_up()
