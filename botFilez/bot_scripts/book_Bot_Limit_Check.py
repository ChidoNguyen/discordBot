
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
def download_history(driver):
    LIMIT_XPATH = {
        "download_history" : "//a[@href='/users/downloads']"
    }
    try:
        click_link = driver.find_element(By.XPATH , LIMIT_XPATH["download_history"])
        href_link = click_link.get_attribute('href')
    except NoSuchElementException as e:
        print(e)
    try:
        driver.get(href_link)
    except:
        print("Download history failed to follow URL.")
    return driver

def limit_check(driver):
    try:
        out_of_ten = driver.find_element(By.CSS_SELECTOR , 'div.m-v-auto.d-count')
    except NoSuchElementException as e:
        print(e)
    str_limit = out_of_ten.text
    if str_limit == "10/10":
        return True
    return False
    
def max_limit(driver):
    return limit_check(download_history(driver))