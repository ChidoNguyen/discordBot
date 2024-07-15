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
        sub_com_args = [env_path , 'bookBot.py', book_details , 'auto']
        outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
        #print(outcome.check_returncode, outcome.stdout, outcome.stderr)
        if outcome.returncode == 0:
            return "OK" , 200
        else:
            return "Nope", 204
        
@app.route('/search_links/', methods = ['POST'])
def search_links():
        book_details = request.json['book_info']
        sub_com_args = [env_path , 'bookBot.py', book_details , 'listings']
        outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
        #print(outcome.check_returncode, outcome.stdout, outcome.stderr)

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
@app.route('/download_url/' , methods = ['POST'])
def download_url():
    url = request.json['book_info']
    subproc_arg = [env_path , 'bookBot.py' , url , 'url']
    outcome = subprocess.run(subproc_arg , capture_output=True, text=True)
    if outcome.returncode == 0:
        response = {
            'status' : "success",
            'response' : 'Download was succesful with given URL.'
        }
        status_code = 200
    else:
        response = {
                'status' : 'Failed',
                'response' : "Book file failed to be created."
        }
        status_code = 400
    return jsonify(response) , status_code
@app.route('/cleanup/',methods = ['GET'])
def cleanup():
    for items in os.listdir(desired_save_dir):
        file_path = os.path.join(desired_save_dir,items)
        if os.path.isfile(file_path) and items.endswith('epub'):
            os.remove(file_path)
    return "cleaned up " , 200
