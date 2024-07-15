from flask import Flask ,jsonify,request
import requests
import subprocess
import os
import platform
import json
from discordCreds import desired_save_dir

app = Flask(__name__)
env_path = './myvenv/Scripts/python' if platform.system() == 'Windows' else "python3" #for windows VSC where env is preset in settings

@app.route('/search_download/',defaults = {'advance' : None} ,  methods = ['POST'])
@app.route('/search_download/<advance>')  
def search_download(advance):
        book_details = request.json['book_info']
        
        if advance:
            sub_com_args = [env_path , 'bookBot.py', book_details , 'listings']
            outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
        #print(outcome.stdout)
            output_path = os.path.join(desired_save_dir,'output.txt')
            if outcome.returncode == 0:
                #sub success == output.txt is generated and created
                try:
                    with open(output_path , 'r') as f:
                        data = f.read().strip()
                    response = {
                        'response' : 'success' ,
                        'data' : data
                    }
                    status_code = 200
                except:
                    response = {
                        'response' : 'bad file',
                        'data' : 'bad file or empty'
                    }
                    status_code = 404
            else:
                response = {
                    'status' : 'Failed',
                    'response' : 'Subprocess failed',

                }
                status_code = 404
            return jsonify(response),status_code
        else:
            sub_com_args = [env_path , 'bookBot.py', book_details , 'auto']
            outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
            if outcome.returncode == 0:
                return "OK" , 200
            else:
                return "Nope", 204
@app.route('/user_choice/' , methods = ['POST'])
def user_choice():
     url_link = request.json['url']
     #spin up a subprocess to run part of our automated script

@app.route('/cleanup/',methods = ['GET'])
def cleanup():
    for items in os.listdir(desired_save_dir):
        file_path = os.path.join(desired_save_dir,items)
        if os.path.isfile(file_path) and items.endswith('epub'):
            os.remove(file_path)
    return "cleaned up " , 200
