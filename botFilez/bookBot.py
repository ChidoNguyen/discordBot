#from selenium import webdriver
import os
import sys
import json
import time
from bot_scripts.book_Bot_Init import driver_setup , login
from bot_scripts.book_Bot_Search import search_input , search_result_data
from bot_scripts.book_Bot_Download import download_attempt , auto_download
from bot_scripts.book_Bot_Limit_Check import max_limit
from botCookies import cookie_epoch , load_cookies , save_cookies
from discordCreds import desired_save_dir , siteURL

'''
Initializes our chrome webdriver to automate the download process 
'''

#!TODO : Splice into "search + results" and "download_choice"
def automated_book_download(user_folder,desired_book,setting_opt):
    #python script "book details" "requester_id"  "settings"
    #settings:
    # 1) listings -> gets a list of links we've acquired
    # 2) auto -> automate top link found download and delivery
    # 3) url -> download from provided URL
    # settings = ['url' , 'auto' , 'listings']
    # if len(sys.argv) != 4:
    #     print("Invalid amount of arguments provided.")
    #     sys.exit(1)
    # if sys.argv[-1] not in settings:
    #     print("Invalid setting argument.")
    #     sys.exit(1)
    # desired_book = sys.argv[1]
    # requester_id = sys.argv[2]
    # #create new folder for user
    # user_folder = os.path.join(desired_save_dir, requester_id)
    # if not os.path.exists(user_folder):
    #     os.makedirs(user_folder)

    ######
    chrome_Driver_Init= driver_setup(user_folder)
    #cookies expiry check if its true ( still valid)
    #cookies and setup always needed for all options provided
    if cookie_epoch():
        load_cookies(chrome_Driver_Init)
        chrome_Driver_Login = chrome_Driver_Init
    else:
        chrome_Driver_Login = login(chrome_Driver_Init)
        save_cookies(chrome_Driver_Login)
    #### !Need to add a 10/10 download limit check ###
    if setting_opt != 'listings' and max_limit(chrome_Driver_Login):
        print("Download limit reached")
        sys.exit(10)
    #return to home page after checking
    chrome_Driver_Login.get(siteURL)
    #if not url we need to search for both auto and listings
    if setting_opt != 'url':
        chrome_Driver_Search = search_input(chrome_Driver_Login , desired_book)
        searchResultData = search_result_data(chrome_Driver_Search) # List of search result links
    if setting_opt == 'listings':
        chrome_Driver_Search.close()
        return searchResultData

    #if we bypass the auto sections we'll have to assign the parameters going into search
    #can either assign it to the same name , or make a new function call with parameter names changed
    if setting_opt == 'url':
        searchResultData = [desired_book] # should be our URL
        chrome_Driver_Search = chrome_Driver_Login
    chrome_Driver_Download_Process = download_attempt(chrome_Driver_Search , searchResultData , user_folder)
    chrome_Driver_Download_Process.close()
    # for items in os.listdir(user_folder):
    #     if items.endswith('.epub'):
    #         return sys.exit()
    # return sys.exit(1)
if __name__ == "__main__":
    settings_options = ['auto' , 'url' , 'listings']
    #argv count = 4 script / book details / requester / setting
    if len(sys.argv) != 4:
        print("Not enough arguments. 'python <script> <book details> <requester> <setting>' ")
        sys.exit(1)
    if sys.argv[-1] not in settings_options:
        print("Not a valid setting options. [ url , auto , listings]")
        sys.exit(1)

    
    desired_book = sys.argv[1]
    requester_id = sys.argv[2]
    settings = sys.argv[-1]
    #create new folder for user
    user_folder = os.path.join(desired_save_dir, requester_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    results = automated_book_download(user_folder,desired_book,settings)

    if sys.argv[-1] == 'listings':
        with open( os.path.join(os.path.join(desired_save_dir, sys.argv[2]) ,"output.txt") , 'w') as f:
            for items in results:
                print(items , file = f)
                #print(items)
        f.close()
        sys.exit()
