from flask import Flask 
from requests import request , jsonify
import subprocess
app = Flask(__name__)

@app.route('/search_download/', methods = ['POST'])
def search_download():
    book_details = request.json()
    try:
        outcome = subprocess.run(['python3' , './bookBot.py'] + book_details, capture_output=True, text = True)
    except Exception as e:
        print(e)

    if outcome : return 'done' , 200
    
    return 'failed' , 204

