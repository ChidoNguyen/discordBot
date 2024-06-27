from flask import Flask ,jsonify,request
import requests
import subprocess
import os
from discordCreds import desired_save_dir

app = Flask(__name__)

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
    for items in os.listdir(desired_save_dir):
        file_path = os.path.join(desired_save_dir,items)
        if os.path.isfile(file_path) and items.endswith('epub'):
            os.remove(file_path)
