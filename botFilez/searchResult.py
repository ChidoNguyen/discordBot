#need to figure out how to search + process the result
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


MAX_RESULT_COUNT = 10
# TODO : Implement bot interaction with script to get wanted book

### search input ####
def search_input(driver,desiredBook):
    XPATH = { 
        's_field' : "//input[@id = 'searchFieldx']",
        's_button' : "//button[@type='submit' and @aria-label='Search']"
    }

    bookInfo = desiredBook

    ### grab input field for search box ###
    try:
        search_field = driver.find_element(By.XPATH, XPATH["s_field"])
    except NoSuchElementException as e:
        print(e)
    
    search_field.send_keys(desiredBook)
    try:
        searchButton = driver.find_element(By.XPATH, XPATH["s_button"]).click()
    except NoSuchElementException as e:
        print(e)
    
    return driver
    

    ###
def search_result_data(driver):


    #each item in search_results cooresponds to an instance of the book we're looking for
    #check english + epub
    #truncate 10 results or if less take as is
    search_results = driver.find_elements(By.CLASS_NAME , 'resItemTable')
    search_results = search_results[:MAX_RESULT_COUNT] if len(search_results) > MAX_RESULT_COUNT else search_results #take top 10 res

    '''
    Code :
    We take our top search reults top 10 or if less then all of them.
    target_divs : had to be hand identified since site jumbles the divs that store file type + language around sometimes ; we pick the class name that identifies what we want
    from our search results - gather the book details section 
    in book details we search thru the child divs class names if we find a match we change the appropriate boolean  value for language/filetype when both are found we store the link to the book
    '''

    ''' CSS_SELECTOR we can pick the HTML CSS tags
        XPATH we treat it more like a true bookDetails (parent) we can search By.XPATH if we say ./div (child div) [contains(@class , 'class_name')]
    '''


    TARGET_DIVS ={'eng' : "property_value text-capitalize" , 'epub' : "property_value" }
    valid_links = []
    for items in search_results:
        bookDetails = items.find_element(By.CLASS_NAME, 'bookDetailsBox') #the site  doesnt have a universal div structure to find english/epub
        lang = fileType = False
        all_divs = bookDetails.find_elements(By.CSS_SELECTOR, 'div')

        #examine the parent div in all_divs for presence of Eng language and epub
        for sub_divs in all_divs:
            class_name = sub_divs.get_attribute('class').strip()
            if class_name == TARGET_DIVS['eng']:
                lang = True
            if class_name == TARGET_DIVS['epub'] and "EPUB" in sub_divs.text:
                fileType = True
            if lang and fileType:
                valid_links.append(items.find_element(By.TAG_NAME , 'a').get_attribute('href'))
                break
    
    #print(*valid_links , sep = '\n')


    return valid_links