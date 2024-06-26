import sys , os , time , json


'''
check if cookie is still valid via expiry epoch

return true if valid false if not 

'''
cookies_path = "./cookies/"
cookies_filename = "bot_cookies.json"
def cookie_epoch():
    #expiry_values = list(int)
    #in line processing assuming cookies arent large data sets
    #save on space
    try:
        with open(cookies_path + cookies_filename, 'r') as file:
            cookies = json.load(file)
            for components in cookies[1:]:
                #seems like first item is time of login which will always be less than epoch-timer so skip it
                if 'expiry' in components and int(components['expiry']) <= int(time.time()):
                    return False
        return True
    except FileNotFoundError:
        return False

def load_cookies(driver):
    with open(cookies_path + cookies_filename,'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            if 'expiry' in cookie and isinstance(cookie['expiry'] , float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
    driver.refresh()

def save_cookies(driver):
    cookies = driver.get_cookies()
    with open(cookies_path + cookies_filename , 'w') as file:
        json.dump(cookies,file)
    
if __name__:
    cookie_epoch()