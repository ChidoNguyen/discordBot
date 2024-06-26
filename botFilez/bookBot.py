#from selenium import webdriver
import os
import sys
import json
import time
from bookFinder import driver_setup , login
from searchResult import search_input , search_result_data
from linkProcessing import auto_download
from discordCreds import desired_save_dir
'''
Initializes our chrome webdriver to automate the download process 
'''
def automated_book_download():
    desired_book = sys.argv[1:]
    chrome_Driver_Init= driver_setup()
    #### todo load cookies
    time.sleep(5)
    with open("./cookies/bot_cookies.json" , 'r') as file:
        cookies = json.load(file)

        #selenium needs expirity attr to be integeer
        for components in cookies:
            if 'expiry' in components and isinstance(components['expiry'],float):
                #recast to int
                components['expiry'] = int(components['expiry'])
            chrome_Driver_Init.add_cookie(components)
    chrome_Driver_Init.refresh()
    time.sleep(30)


    #### todo end###
    #chrome_Driver_Login = login(chrome_Driver_Init)

    # TODO : Cookies for login state #
    # cookies = chrome_Driver_Login.get_cookies()
    # with open("./cookies/bot_cookies.json" , 'w') as file:
    #     json.dump(cookies,file)
    # return 1

    ##### TODO#####
    chrome_Driver_Search = search_input(chrome_Driver_Login , desired_book)
    searchResultData = search_result_data(chrome_Driver_Search) # List of search result links
    if not searchResultData:
        print("No results found")
    else:    
        chrome_Driver_Download_Process = auto_download(chrome_Driver_Search , searchResultData)

    chrome_Driver_Download_Process.close()
    for items in os.listdir(desired_save_dir):
        if items.endswith('.epub'):
            return True
    return False
if __name__ == "__main__":
    automated_book_download()