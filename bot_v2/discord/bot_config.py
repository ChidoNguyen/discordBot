import configparser

config = configparser.ConfigParser()
config.read('bot_config.ini')

USER_KEY = config.get('Discord','userKey')