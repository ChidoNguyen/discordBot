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

def download_attempt(driver,searchLinks):
    for items in searchLinks:
        driver.get(items)
        if auto_download(driver):
            return driver
    return driver
def auto_download(driver):
    
    try:
        download_link = None
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

        dropDownMenuOptions = driver.find_elements(By.XPATH , "//a[contains(@class , 'addDownloadedBook')]")
        
        #assuming first choice matches the search result file type we want
        dropDownMenuOptions[1].click()

        download_incomplete = True
        time.sleep(5)
        timeout_sec = 0
        while download_incomplete  and timeout_sec < 45:
            #while not done check for file 
            for file_names in os.listdir(desired_save_dir):
                if file_names.endswith(".epub"):
                    download_incomplete = False
            time.sleep(1)
            timeout_sec += 1
        print("????")
        return True
    except:
        return False
    
    
    #TODO : MIGHT NEED TO EDIT IF OUR page which should be EPUB isnt first download choice
    



#new_button_edit()