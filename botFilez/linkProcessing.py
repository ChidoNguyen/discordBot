from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException

import os
import time
from discordCreds import desired_save_dir
#url link input
def lp(driver):
    bookURL = "https://z-library.rs/book/28168813/d7121c/the-anxious-generation.html"

    #driver = webdriver.Chrome()
    driver.get(bookURL)

    #wait for download link to be avail
    try:
        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary.addDownloadedBook")))
    except NoSuchElementException:
        print("Failed to find download element.")
    
    #grab the link#

    try:
        urlLink = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary.addDownloadedBook").get_attribute('href')
    except NoSuchElementException:
        print("Link not found.")

    #find author book title
    #book author might be anchored in "h1" with
    try:
        driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary.addDownloadedBook")#.click()
    except:
        print("rip")
    book_title = driver.find_element(By.TAG_NAME,'h1').text
    author_text = driver.find_element(By.XPATH , '//a[@class = "color1"]').text
    file_saved_name = book_title + "_____" + author_text
    ext_ending = ".crdownload"

    #few approaches either wait for our file to appear via .epub showing up 
    # or until crdownload ceases to exist
    # for now only 1 file will exist at a time so we can do either
    # if storing multiple books or unfinished download multiple epub/crdownload may exist
    download_incomplete = True
    time.sleep(120)
    while download_incomplete:
        #while not done check for file 
        for file_name in os.listdir(desired_save_dir):
            if file_name.endswith('.epub'):
                download_incomplete = False
    print("????")
    return
