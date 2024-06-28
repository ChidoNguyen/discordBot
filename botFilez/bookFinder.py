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

import linkProcessing as downProc
from searchResult import search_input
from discordCreds import siteURL , userID , userPASS , desired_save_dir

####setup######
#initialize our chrome driver with preferences/options
#?Params : None
#!Returns : chrome webdriver object
###############
def driver_setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    prefs = {
        "download.default_directory" : desired_save_dir ,
        "savefile.default_directory" : desired_save_dir , 
        "download.prompt_for_download" : False ,
        "directory_upgrade" : True
    }
    options.add_experimental_option("prefs", prefs)
    service = Service(executable_path = 'usr/bin/chromedriver')
    driver = webdriver.Chrome(service = service , options = options)

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

    try:
        navBarById = driver.find_element(By.ID , "profileMenu")
        navBarById.click()
    except NoSuchElementException:
        print("No Element")
    except TimeoutException:
        print("Timed Out")

    #######################
    # Logged Verification #
    try:
        driver.find_element(By.XPATH, "//a[@href='/logout.php']")
        return driver
    except:
        print("login failed")
        return None
    



