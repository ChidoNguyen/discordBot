"""
Automation to login / search / download / and deliver desired publication

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from discordCreds import siteURL , userID , userPASS


driver = webdriver.Chrome()
driver.get(siteURL) #fill with our url

try:
    assert "Z-Library" in driver.title
except:
    print(f'Bad URL : {siteURL}')

#scoure the site for "a href" so we can go thru it for login redirection
aHref = driver.find_element(By.TAG_NAME,'a href')

for a in aHref:
    if "login" in a:
        print(a)


driver.close()