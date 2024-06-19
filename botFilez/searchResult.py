#need to figure out how to search + process the result
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


MAX_RESULT_COUNT = 10
# TODO : Implement bot interaction with script to get wanted book
def bot_search_input():
    return {"author" : "Blake Crouch" , "title" : "Recursion"}

### search input ####
def search_input():
    XPATH = { 
        's_field' : "//input[@id = 'searchFieldx']",
        's_button' : "//button[@type='submit' and @aria-label='Search']"
    }
    driver = webdriver.Chrome()
    driver.get("https://z-library.rs/")
    bookInfo = bot_search_input()
    author = bookInfo["author"]
    title = bookInfo["title"]

    ### grab input field for search box ###
    try:
        search_field = driver.find_element(By.XPATH, XPATH["s_field"])
    except NoSuchElementException as e:
        print(e)
    
    search_field.send_keys(author + " " + title)
    try:
        searchButton = driver.find_element(By.XPATH, XPATH["s_button"]).click()
    except NoSuchElementException as e:
        print(e)
    

    

    ###
def searchInput():
    testUrl = "https://z-library.rs/s/Blake%20Crouch%20Recursion/?languages%5B0%5D=english"
    driver = webdriver.Chrome()
    driver.get(testUrl)

    #each item in search_results cooresponds to an instance of the book we're looking for
    #check english + epub
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


    target_divs ={'eng' : "property_value text-capitalize" , 'epub' : "property_value" }
    valid_links = []
    for items in search_results:
        bookDetails = items.find_element(By.CLASS_NAME, 'bookDetailsBox') #the site  doesnt have a universal div structure to find english/epub
        lang = fileType = False
        all_divs = bookDetails.find_elements(By.CSS_SELECTOR, 'div')

        for sub_divs in all_divs:
            class_name = sub_divs.get_attribute('class').strip()
            if class_name == target_divs['eng']:
                lang = True
            if class_name == target_divs['epub'] and "EPUB" in sub_divs.text:
                fileType = True
            if lang and fileType:
                valid_links.append(items.find_element(By.TAG_NAME , 'a').get_attribute('href'))
                break
    
    #print(*valid_links , sep = '\n')


    driver.close()

search_input()