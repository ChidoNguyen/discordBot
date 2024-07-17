"""
Automation to login / search / download / and deliver desired publication

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException   
from selenium.webdriver.chrome.service import Service

import time
import platform
import linkProcessing as downProc
from searchResult import search_input
from discordCreds import siteURL , userID , userPASS , desired_save_dir
from limit_check import download_history , limit_check
####setup######
#initialize our chrome driver with preferences/options
#?Params : None
#!Returns : chrome webdriver object
###############
def driver_setup():
    
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    #options.add_argument('--disable-gpu')
    prefs = {
        "download.default_directory" : desired_save_dir ,
        "savefile.default_directory" : desired_save_dir , 
        "download.prompt_for_download" : False ,
        "directory_upgrade" : True
    }
    options.add_experimental_option("prefs", prefs)
    if platform.system() in ['Linux']:
        service = Service('/usr/bin/chromedriver')
        options.binary_location('/usr/bin/chromium-browser')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service,options = options)
    else:
        driver = webdriver.Chrome(options=options)
    #driver.set_window_rect(width=1200, height=900)
    ##############

    driver.get(siteURL) #fill with our url
    driver.implicitly_wait(10)

    try:
        assert "Z-Library" in driver.title
        return driver
    except:
        print(f'Bad URL : {siteURL}')
        return None

    
#### login ####
#? Param : web driver
#! Returns : updated driver after verifying login is successful
#####
def login(driver):
    login_div = driver.find_element(By.CLASS_NAME, "user-data__sign")
    anchor_elem = login_div.find_element(By.TAG_NAME,'a')
    login_url = anchor_elem.get_attribute('href')

    # login page #
    driver.get(login_url)
    login_form = driver.find_element(By.TAG_NAME, "form")
    #form_inputs = login_form.find_elements(By.TAG_NAME, "input")
    idEntry = login_form.find_element(By.NAME , 'email')
    passwordEntry = login_form.find_element(By.NAME, 'password')
    submitButton = login_form.find_element(By.TAG_NAME, 'button')

    #login
    idEntry.send_keys(userID)
    passwordEntry.send_keys(userPASS)
    submitButton.click()

    ################### drop down menu hidden #####################
    #grab the nav bar "icon" element
    #same outcome as By.ID but potentially slower and our project is not that intensive
    #navBar = driver.find_element(By.XPATH, "//*[@id = 'profileMenu']")

    # try:
    #     navBarById = driver.find_element(By.ID , "profileMenu")
    #     navBarById.click()
    # except NoSuchElementException:
    #     print("No Element")
    # except TimeoutException:
    #     print("Timed Out")

    #######################
    # Logged Verification #
    try:
        driver.find_element(By.XPATH, "//a[@href='/logout.php']")
        return driver
    except:
        print("login failed")
        return None
    


if __name__ == '__main__':
    mydrive = login(driver_setup())
    
    limit_check(download_history(mydrive))