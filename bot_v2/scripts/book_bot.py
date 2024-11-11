
import sys,os
from book_bot_config import download_dir
from auto_bot_setup import auto_bot
#will probably use command line arguments to trigger specific user requested processes
#example "[python] [script_name.py] [search term/phrase] [requester] [settings]""
BOT_SETTINGS = ['getbook', 'getbook-adv', 'pick']

def book_bot():
    if len(sys.argv) != 4:
        print(f'Invalid number of arguments. Expected 4 , only got {len(sys.argv)}.')
        sys.exit(1)
    if sys.argv[-1] not in BOT_SETTINGS:
        print(f'Invalid setting argument used.')
        sys.exit(1)

    book_search_string = sys.argv[1]
    requester_id = sys.argv[2]

    #create folder with user's ign for selenium webdriver to use as a download path location
    user_folder_path = os.path.join(download_dir, requester_id)
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)
    
    #create selenium driver
    bot_driver = auto_bot(user_folder_path)
