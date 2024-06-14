from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException

PREF = {"download_dir" : ""}
#url link input
def lp(driver):
    bookURL = "https://z-library.rs/book/28168813/d7121c/the-anxious-generation.html"

    #driver = webdriver.Chrome()
    driver.get(bookURL)
    try:
        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary.addDownloadedBook")))
        driver.alert()
    except NoSuchElementException:
        print("failed download")

    return
