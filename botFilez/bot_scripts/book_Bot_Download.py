from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException

import os
import time
#from discordCreds import desired_save_dir
#url link input

def download_attempt(driver,searchLinks,user_folder):
    for items in searchLinks:
        driver.get(items)
        if auto_download(driver,user_folder):
            return driver
    return driver

def rename_file(book,author,user_folder):
    try:
        import re
        book = re.sub(r'[<>:"/\\|?*]', ' ',book)
        all_files = [os.path.join(user_folder,f) for f in os.listdir(user_folder)]
        newest = max(all_files, key=os.path.getctime)
        os.rename(os.path.join(user_folder,newest), os.path.join(user_folder, f'{book} by {author}.epub'))
    except Exception as e:
        print(e)
        
def auto_download(driver,desired_save_dir):
    
    try:
        #this section is still fine since the download section is still viable 
        try:
            wait = WebDriverWait(driver,10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary.addDownloadedBook")))
        except NoSuchElementException:
            print("Failed to find download element.")
        
        #need to click "..." next to the old download now button to go to drop down menu

        try:
            dropDown = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.dropdown-toggle.dlDropdownBtn")
            dropDown.click()
        except NoSuchElementException as e:
            print(e)
        
    #driver too fast need to delay for li to show up
        # try:
        #     wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class = 'addDownloadedBook']")))
        # except NoSuchElementException as e:
        #     print(e)
        # except:
        #     print("doode")
        ############### extract list items
        #could grab book info prior to downloading
        #title/author to rename files w/o bloated text
        try:
            book_name = driver.find_element(By.XPATH , '//h1[@itemprop = "name"]').text
            author_name = driver.find_element(By.XPATH, '//a[@class = "color1"][@title="Find all the author\'s book"]').text
            #rint(book_name,author_name)   
        except Exception as e:
            print(e)
        dropDownMenuOptions = driver.find_elements(By.XPATH , "//a[contains(@class , 'addDownloadedBook')]")
        #assuming first choice matches the search result file type we want
        dropDownMenuOptions[1].click()
        download_incomplete = True
        time.sleep(5)
        timeout_counter = 0
        timeout_max = 60 #sec
        while download_incomplete and timeout_counter < timeout_max:
            download_incomplete = False
            for file_names in os.listdir(desired_save_dir):
                if file_names.endswith('.crdownload'):
                    download_incomplete = True
            timeout_counter += 1
            time.sleep(1)
        
        if not download_incomplete:
            rename_file(book_name,author_name,desired_save_dir)
        # download_incomplete = True
        # time.sleep(5)
        # timeout_sec = 0
        # while download_incomplete  and timeout_sec < 45:
        #     #while not done check for file 
        #     for file_names in os.listdir(desired_save_dir):
        #         if file_names.endswith(".epub"):
        #             download_incomplete = False
        #     time.sleep(1)
        #     timeout_sec += 1
        return True
    except Exception as e:
        print(e)
        return False
    
    
    #TODO : MIGHT NEED TO EDIT IF OUR page which should be EPUB isnt first download choice
    



#new_button_edit()