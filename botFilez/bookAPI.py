from flask import Flask ,jsonify,request
import requests
import subprocess
import os
import sys
from discordCreds import desired_save_dir , adminID

app = Flask(__name__)

@app.route('/search_download/', methods = ['POST'])
def search_download():

        book_details = request.json['book_info']
        if not book_details:
             return "Missing 'book_info' in request body" , 400
        
        sub_com_args = ['python3' , './bookBot.py', book_details]
        outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
        if outcome.returncode == 0:
            return "OK" , 200
        else:
            return "Failed to process request" , 500
        
@app.route('/cleanup/',methods = ['GET'])
def cleanup():
    for items in os.listdir(desired_save_dir):
        file_path = os.path.join(desired_save_dir,items)
        if os.path.isfile(file_path) and items.endswith('epub'):
            os.remove(file_path)
    return "Cleanup completed" , 200

@app.route('/shutdown/<admin_ID>' , methods = ['GET'])
def shut_it(admin_ID):
    if adminID != int(admin_ID):
         return "Unauthorized" , 401
    return "Shutdown initiated" , 200
     
if __name__ == '__main__':
    app.run(debug=True)

        