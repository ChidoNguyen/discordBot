"""
Automation to login / search / download / and deliver desired publication

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from discordCreds import siteURL , userID , userPASS


driver = webdriver.Chrome()
driver.get('https://www.mozilla.org/en-US/firefox/new/?redirect_source=firefox-com') #fill with our url

# try:
#     assert "Z-Library" in driver.title
# except:
#     print(f'Bad URL : {siteURL}')

#scoure the site for "a href" so we can go thru it for login redirection
aHref = driver.find_elements(By.TAG_NAME,'a')

loginURL = ""

#links = [href.get_attribute('href') for items in aHref]
#print(links)
for items in aHref:
    if "login" in (items.get_attribute('href')).lower():
        print("found login")
driver.close()