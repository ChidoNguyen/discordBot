"""
Automation to login / search / download / and deliver desired publication

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from discordCreds import siteURL , userID , userPASS


driver = webdriver.Chrome()
driver.get(siteURL) #fill with our url

try:
    assert "Z-Library" in driver.title
except:
    print(f'Bad URL : {siteURL}')

#find the specific div hosting login link , grab the anchor, then grab the url#
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
print(idEntry,passwordEntry)
idEntry.send_keys(userID)
passwordEntry.send_keys(userPASS)
submitButton.click()

#explicit wait for page to redirect
errors = [NoSuchElementException]
wait = WebDriverWait(driver, timeout = 2, poll_frequency = .2 , ignore_exceptions = errors)
wait.until(driver.find_element(By.LINK_TEXT, 'logout'))
print(driver.title)


#driver.close()