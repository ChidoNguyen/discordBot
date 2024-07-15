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
    #python script "book details" "settings"
    #settings:
    # 1) listings -> gets a list of links we've acquired
    # 2) auto -> automate top link found download and delivery
    # 3) url -> download from provided URL
    if len(sys.argv) != 3:
        print("Invalid amount of arguments provided.")
    desired_book = sys.argv[1]
    chrome_Driver_Init= driver_setup()

    #cookies expiry check if its true ( still valid)
    #cookies and setup always needed for all options provided
    if cookie_epoch():
        load_cookies(chrome_Driver_Init)
        chrome_Driver_Login = chrome_Driver_Init
    else:
        chrome_Driver_Login = login(chrome_Driver_Init)
        save_cookies(chrome_Driver_Login)
    #if not url we need to search for both auto and listings
    if sys.argv[-1] != 'url':
        chrome_Driver_Search = search_input(chrome_Driver_Login , desired_book)
        searchResultData = search_result_data(chrome_Driver_Search) # List of search result links
    if sys.argv[-1] == 'listings':
        chrome_Driver_Search.close()
        return searchResultData

    #if we bypass the auto sections we'll have to assign the parameters going into search
    #can either assign it to the same name , or make a new function call with parameter names changed
    if sys.argv[-1] == 'url':
        searchResultData = [sys.argv[1]] # should be our URL
        chrome_Driver_Search = chrome_Driver_Login
    chrome_Driver_Download_Process = download_attempt(chrome_Driver_Search , searchResultData)

    chrome_Driver_Download_Process.close()
    for items in os.listdir(desired_save_dir):
        if items.endswith('.epub'):
            return sys.exit()
    return sys.exit(1)
if __name__ == "__main__":
    results = automated_book_download()

    if sys.argv[-1] == 'listings':
        with open( os.path.join(desired_save_dir ,"output.txt") , 'w') as f:
            for items in results:
                print(items , file = f)
                #print(items)
