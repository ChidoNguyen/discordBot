"""
Automation to login / search / download / and deliver desired publication

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from discordCreds import siteURL , userID , userPASS


driver = webdriver.Chrome()
driver.get(siteURL) #fill with our url




driver.close()