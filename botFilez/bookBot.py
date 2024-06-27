#from selenium import webdriver
import os
import sys
import json
import time
from bookFinder import driver_setup , login
from searchResult import search_input , search_result_data
from linkProcessing import download_attempt
from botCookies import cookie_epoch , load_cookies , save_cookies
from discordCreds import desired_save_dir
'''
Initializes our chrome webdriver to automate the download process 
'''
def automated_book_download():
    desired_book = sys.argv[1:]
    chrome_Driver_Init= driver_setup()

    #cookies expiry check if its true ( still valid)
    if cookie_epoch():
        load_cookies(chrome_Driver_Init)
        chrome_Driver_Login = chrome_Driver_Init
    else:
        chrome_Driver_Login = login(chrome_Driver_Init)
        save_cookies(chrome_Driver_Login)

    chrome_Driver_Search = search_input(chrome_Driver_Login , desired_book)
    searchResultData = search_result_data(chrome_Driver_Search) # List of search result links
    
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
    automated_book_download()