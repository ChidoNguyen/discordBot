from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import platform , configparser , time
import bot_site_cookies

def auto_bot_driver(save_dir):
    #chrome driver options
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless") #no window open during script run
    prefs = {
        "download.default_directory" : save_dir ,
        "savefile.default_directory" : save_dir , 
        "download.prompt_for_download" : False ,
        "directory_upgrade" : True
    }
    options.add_experimental_option('prefs',prefs)
    ###

    bot_driver = None
    if platform.system() == 'Linux': #platform dependent initilization
        service = Service('/usr/bin/chromedriver')
        bot_driver = webdriver.Chrome(service=service , options=options)
    else:
        bot_driver = webdriver.Chrome(options=options)

    return bot_driver

def homepage(bot_driver):
    config = configparser.ConfigParser()
    config.read('book_bot_config.ini')
    site_url = config.get('WEB','url')

    bot_driver.get(site_url)
    bot_driver.implicitly_wait(10)
    
    if "Z-Library" in bot_driver.title:
        return bot_driver
    return None

def login_page(bot_driver):
    login_html_text = {
        'login-div' : 'user-data__sign',

    }
    #login page link
    try:
        login_link_div = bot_driver.find_element(By.CLASS_NAME , login_html_text['login-div'])
        anchor_element = login_link_div.find_element(By.TAG_NAME, 'a')
        login_link = anchor_element.get_attribute('href')
        bot_driver.get(login_link) #navigate to login page
        return bot_driver
    except:
        print(f'Failed to identify link for login page.')
        return None

    #login form
def login_creds_input(bot_driver):
    config = configparser.ConfigParser()
    config.read("book_bot_config.ini")
    uID , uPass = config.get("WEB",'userID'), config.get("WEB",'userPass')

    login_form = bot_driver.find_element(By.TAG_NAME, "form")
    idEntry = login_form.find_element(By.NAME, 'email').send_keys(uID)
    passEntry = login_form.find_element(By.NAME, 'password').send_keys(uPass)
    submitButton = login_form.find_element(By.TAG_NAME, 'button').click()

    try:
        bot_driver.find_element(By.XPATH, "//a[@href='/logout.php']")
        return bot_driver
    except:
        print("login attempt failed")
        return None

def test_auto_bot():
    return

def auto_bot(save_dir):
    ab_driver = auto_bot_driver(save_dir) #setup our initial webdriver client
    homepage_driver = login_element_driver = logged_in_driver = None
    if ab_driver:
        homepage_driver = homepage(ab_driver)

    #cookies check to see if login is needed
    if bot_site_cookies.valid_cookies():
        bot_site_cookies.load_cookies(homepage_driver)
        return homepage_driver
    else:
        if homepage_driver:
            login_element_driver = login_page(homepage_driver)
        if login_element_driver:
            logged_in_driver = login_creds_input(login_element_driver)
        bot_site_cookies.save_cookies(logged_in_driver)
        return logged_in_driver


auto_bot('./cookies')