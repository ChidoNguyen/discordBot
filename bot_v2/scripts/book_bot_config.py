import configparser

config = configparser.ConfigParser()
config.read("book_bot_config.ini")
download_dir = config.get("User" , "download_dir")