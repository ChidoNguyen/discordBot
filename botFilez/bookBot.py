#from selenium import webdriver
import os
import sys
import json
import time
from bookFinder import driver_setup , login
from searchResult import search_input , search_result_data
from linkProcessing import download_attempt , auto_download
from botCookies import cookie_epoch , load_cookies , save_cookies
from discordCreds import desired_save_dir
'''
Initializes our chrome webdriver to automate the download process 
'''

#!TODO : Splice into "search + results" and "download_choice"
def automated_book_download():
    if len(sys.argv) < 3:
        print("Not enough arguments provided.")
        sys.exit(1)

    adv_option = sys.argv[-1]
    #listings => output txt
    #auto => run whole script
    # url => url downloader
    desired_book = sys.argv[1]
    chrome_Driver_Init= driver_setup()

    #cookies expiry check if its true ( still valid)
    if cookie_epoch():
        load_cookies(chrome_Driver_Init)
        chrome_Driver_Login = chrome_Driver_Init
    else:
        chrome_Driver_Login = login(chrome_Driver_Init)
        save_cookies(chrome_Driver_Login)

    if adv_option == 'url':
        chrome_Driver_Download_Process = auto_download(chrome_Driver_Login.get(sys.argv[1]))
        chrome_Driver_Login.close()
        return 

    chrome_Driver_Search = search_input(chrome_Driver_Login , desired_book)
    searchResultData = search_result_data(chrome_Driver_Search) # List of search result links
    if adv_option == 'listings':
        return searchResultData

    ######### splice here #######
    if not searchResultData:
        print("No results found")
    else:    
        chrome_Driver_Download_Process = download_attempt(chrome_Driver_Search , searchResultData)

    chrome_Driver_Download_Process.close()
    for items in os.listdir(desired_save_dir):
        if items.endswith('.epub'):
            return True
    return False
if __name__ == "__main__":
    results = automated_book_download()
    if sys.argv[-1] == 'listings':
        with open( os.path.join(desired_save_dir ,"output.txt") , 'w') as f:
            for items in results:
                print(items , file = f)
                #print(items)
