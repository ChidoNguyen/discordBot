import configparser

config = configparser.ConfigParser()
config.read("config.ini")

USER_KEY = config.get('Discord','userKey')
USER_ID = config.get('Discord', 'userID')
USER_PASS = config.get('Discord','userPass')
DISCORD_ADMIN_ID = config.get('Discord','adminID')

SITE = config.get('Webpage','siteURL')

SAVE_DIR = config.get('Local','saveDir')


CONFIG = {
    'USER_KEY' : USER_KEY,
    'USER_ID' : USER_ID,
    'USER_PASS' : USER_PASS,
    'DISCORD_ADMIN_ID' : DISCORD_ADMIN_ID,
    'SITE' : SITE,
    'SAVE_DIR' : SAVE_DIR
}

