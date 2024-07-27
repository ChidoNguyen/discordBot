from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException


import os , sys
import time
import shutil
#from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

#create an event handler that listens for when (for our code) a file is created
#hence the check for is not a directory
#we create event handler Observer obj. run our script
#join and close when everything is done
class DownloadHandler(FileSystemEventHandler):
    def __init__(self,target_name,download_dir):
        self.target_name = target_name
        self.success = False
        self.download_dir = download_dir
    
    def on_created(self,event):
        if not event.is_directory:
            file_path = event.src_path  # source path of what triggered the event aka our "new download"
            ##wait until our file download is finished##
            try:
                timeout = 0
                download_incomp = True
                time.sleep(5)
                if not download_incomp:
                    self.success = True
                try:
                    new_file_path = os.path.join(self.download_dir ,self.target_name)
                    shutil.move(file_path,new_file_path)
                except Exception as e:
                    print(e)
                
            except Exception as e:
                print(e)
                print("File failed to download.")

#from discordCreds import desired_save_dir
#url link input

def download_attempt(driver,searchLinks,user_folder):
    for items in searchLinks:
        driver.get(items)
        if auto_download(driver,user_folder):
            return driver
    return driver
def auto_download(driver,desired_save_dir):
    try:
        author , title = author_title_extract(driver)
    except Exception as e:
        print(e)
        return
    ##set up our observer
    observer = Observer()
    file_name = title + " - " + author + ".epub"
    event_handler = DownloadHandler(file_name,desired_save_dir)
    observer.schedule(event_handler,path=desired_save_dir,recursive = False)
    observer.start()
    success_status = False
    try:
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
        time.sleep(5)
        #download should be taken over by the observer event handler
        #download_incomplete = True
        #time.sleep(5)
        
        # timeout_sec = 0
        # while download_incomplete  and timeout_sec < 45:
        #     #while not done check for file 
        #     for file_names in os.listdir(desired_save_dir):
        #         if file_names.endswith(".epub"):
        #             download_incomplete = False
        #     time.sleep(1)
        #     timeout_sec += 1
        success_status = event_handler.success
    finally:
        observer.stop()
        observer.join()
    return success_status
        
    
    
    #TODO : MIGHT NEED TO EDIT IF OUR page which should be EPUB isnt first download choice
    
def author_title_extract(driver):
    #title located in HTML component <h1> with an itemprop attribute , value = 'name'
    #author is located under <i> tag to italicize name
    #author - class = color1 // title = "Find all the author's book"
    try:
        title_comp = driver.find_element(By.CSS_SELECTOR , "h1[itemprop='name']")
        title_text = title_comp.text
    except Exception as e:
        print(e)
        print("Error inside title extraction attempt.")
    try:
        author_comp = driver.find_element(By.CSS_SELECTOR , "a[class='color1'][title=\"Find all the author's book\"]")
        author= author_comp.text
    except Exception as e:
        print(e)
        print("Error inside author extraction.")
    return author , title_text

if __name__ == '__main__':
    if sys.argv[-1] == 'title':
        author_title_extract(sys.argv[-2])
#new_button_edit()