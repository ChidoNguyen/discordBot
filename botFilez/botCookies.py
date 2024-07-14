import sys , os , time , json


'''
check if cookie is still valid via expiry epoch

return true if valid false if not 

'''
cookies_path = "./cookies/"
cookies_filename = "bot_cookies.json"

def cookie_epoch():
    
    #makes directory if it hasnt already been made#
    try:
        os.makedirs(cookies_path,exist_ok=True)
    except Exception as e:
        print(e)
    
    #check expiration of cookies login values
    #if expired or not found return False
    #if still valid True
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

#loads previously saved cookies 
def load_cookies(driver):
    with open(cookies_path + cookies_filename,'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            if 'expiry' in cookie and isinstance(cookie['expiry'] , float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
    driver.refresh()

#dumps current cookies from driver session to refresh/update expired or missing cookies.
def save_cookies(driver):
    cookies = driver.get_cookies()
    with open(cookies_path + cookies_filename , 'w') as file:
        json.dump(cookies,file)
    
if __name__:
    cookie_epoch()