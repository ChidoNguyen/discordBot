
import sys,os
from auto_bot_setup import auto_bot
from auto_bot_util import max_limit
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

    #initialize selenium webdriver 
    bot_driver = auto_bot(requester_id)

    #download limit check
    if max_limit(bot_driver):
        print(f'Download limit reached.')
        sys.exit(10)

    '''
    Search
    DL
    ---
    Search
    return search result
    ---
    pick from search results
    '''
    

