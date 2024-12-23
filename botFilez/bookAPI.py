from flask import Flask ,jsonify,request
import requests
import subprocess , multiprocessing
import os
import platform
import json
from discordCreds import desired_save_dir
from werkzeug.serving import make_server

app = Flask(__name__)
ENV_PATH = './myvenv/Scripts/python' if platform.system() == 'Windows' else "python3" #for windows VSC where env is preset in settings
server = None
#blocking fix?

#separate the app route + the subprocess with a subprocess_func
def sd_subprocess(book_details, book_requester , result_queue):
    sub_com_args = [ENV_PATH , 'bookBot.py', book_details , book_requester , 'auto']
    outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
    result_queue.put(outcome.returncode)

@app.route('/online' , methods = ['GET'])
def online():
    return "Online" , 200
@app.route('/search_download/', methods = ['POST'])
def search_download():
    book_details = request.json['book_info']
    book_requester = request.json['requester']
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target= sd_subprocess, args=(book_details,book_requester,result_queue))
    process.start()
    process.join()
    return_code = result_queue.get()
    if return_code == 0:
        return "Search and download succesful." , 200
    elif return_code == 10:
        return "Download limit reached." , 405
    else:
        return "Search and download failed." , 204
    ##outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
    #print(outcome.check_returncode, outcome.stdout, outcome.stderr)
    # if outcome.returncode == 0:
    #     return "OK" , 200
    # else:
    #     return "Nope", 204
        
@app.route('/search_links/', methods = ['POST'])
def search_links():
    book_details = request.json['book_info']
    requester = request.json['requester']
    sub_com_args = [ENV_PATH , 'bookBot.py', book_details, requester , 'listings']
    outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
    #print(outcome.check_returncode, outcome.stdout, outcome.stderr)

    #print(outcome.stdout)
    user_folder = os.path.join(desired_save_dir,requester)
    output_path = os.path.join(user_folder,'output.txt')
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
    elif outcome.returncode == 10:
        response = {
            'response' : 'failed',
            'data' : 'Download limit reached.'
        }
        status_code = 405
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
    requester = request.json['requester']
    subproc_arg = [ENV_PATH , 'bookBot.py' , url , requester, 'url']
    outcome = subprocess.run(subproc_arg , capture_output=True, text=True)
    if outcome.returncode == 0:
        response = {
            'status' : "success",
            'response' : 'Download was succesful with given URL.'
        }
        status_code = 200
    elif outcome.returncode == 10:
        response = {
            'status' : 'Failed',
            'response' : 'Download limit reached.'
        }
        status_code = 405
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
    if os.path.isfile(os.path.join(desired_save_dir,'output.txt')):
        os.remove(os.path.join(desired_save_dir,'output.txt'))
    return "cleaned up " , 200

def start_app():
    app.run()
