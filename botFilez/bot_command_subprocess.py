import discord
from discord.ext import tasks
import requests , json
import os , time , datetime
import concurrent.futures
import discordCreds as creds

API_END = { 'api' : "http://localhost:5000/" ,
            'download' : "search_download/",
            'listing' : "search_links/",
            'pick' : "download_url/",
            'cleanup' : "cleanup"
           }
#search folder should only have 1 epub currently, grabs it and create file for discord bot to attach/upload
def discord_file_creation():
    myfile = None
    for items in os.listdir(creds.desired_save_dir):
        if items.endswith('epub'):
            myfile = items
    joined_path = os.path.join(creds.desired_save_dir , myfile)
    with open(joined_path , 'rb') as discordFile:
        attached_file = discord.File(fp = discordFile , filename=myfile)
    return attached_file


#download_book for !getbook
'''
param search_str : parsed message user input for bot to search has the !command portion removed
param requester : is a discord message object to identify user id/name
'''
def download_book(search_str , requester ):
    #request book
    #make file
    #if successful send info back
    #else error messages
    data = {'book_info' : search_str}
    try:
        response = requests.post(API_END['api'] + API_END['download'] , json=data)
    except:
        print(f'{response.text}')
    if response.status_code == 200:
        book_file = discord_file_creation()
        return book_file , f"{requester.mention}"
    elif response.status_code == 405:
        return f'Download limit reached. {requester.mention}'
    else:
        return f'Failed to get book : {search_str} {requester.mention}'


def search_results(search_str,requester,user_state):
    data = {'book_info' : search_str}
    try:
        response = requests.post(API_END['api'] + API_END['listing'] , json=data)
    except:
        print(f'{response.text}')
    json_response_payload = json.loads(response.content)
    processed_response = json_response_payload['data'].split()
    if not processed_response:
        return f'No results were found. {requester.mention}'
    elif response.status_code == 200:
        user_state.book_options = processed_response
        format_msg = ""
        for idx,items in enumerate(processed_response , start = 1):
            format_msg += f'{idx}. <{items}>\n'
        format_msg += f'{requester.mention}'

        return format_msg
    elif response.status_code == 400:
        return f'Bad results file. {requester.mention}'
    

def search_results_download(user_choice , requester , user_state):
    user_choice_url = user_state.book_options[user_choice]
    data = {'book_info' : user_choice_url}
    response = requests.post(API_END['api'] + API_END['pick'] , json=data)
    if response.status_code == 200:
        file_obj = discord_file_creation()
        return file_obj, f'{requester.mention}'
    elif response.status_code == 405:
        return f'Download limit reached. {requester.mention}'
    else:
        return f'Failed to get book. {requester.mention}'
    