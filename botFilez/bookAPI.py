from flask import Flask ,jsonify,request
import requests
import subprocess
app = Flask(__name__)

@app.route('/search_download/', methods = ['POST'])
def search_download():
        book_details = request.json['book_info']
        sub_com_args = ['python3' , './bookBot.py', book_details]
        outcome = subprocess.run(sub_com_args, capture_output=True, text = True)
        if outcome.statuscode == 0:
            return "OK" , 200
        else:
            return "Nope", 204