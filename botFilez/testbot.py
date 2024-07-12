import discord
import discordCreds as creds
import requests
import os
import json

#bot permissions#
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

#some housekeeping items and discord server specific for internal usage#
GUILD = "Janitors Guild"
API_ENDPOINT = { 'api' : "http://localhost:5000/"}
ALLOWED_CHANNEL = ['im-testing-shit-ignore-me-chido']
USER_ID = {'kkot' : 705999688893071430, 'jonathan': 137004891360067584}
COMMAND_PREFIX = "!"
commands ={}

#user states
user_states = {}

class UserStates :
    def __init__(self):
        self.cancel_flag = False
        self.task = None
        self.book_options = []

def command(name):
    def decorator(func):
        commands[name] = func
        return func
    return decorator

##### * * ###################
def discord_file_creation():
    myfile = None
    for items in os.listdir(creds.desired_save_dir):
        if items.endswith('epub'):
            myfile = items
    joined_path = os.path.join(creds.desired_save_dir , myfile)
    with open(joined_path , 'rb') as discordFile:
        attached_file = discord.File(fp = discordFile)
    return attached_file
#on ready for when the bot has successfully joined a server/guild
@client.event
async def on_ready():
    #guild = discord.utils.find(lambda g : g.name == "Janitors Guild" , client.guilds)
    #abstraction of utils.find
    guild = discord.utils.get(client.guilds, name = GUILD)
    print(f'We have logged in as {client.user}. Server : {guild.name} , {guild.id}')


@client.event
async def on_message(message):
    #pretty much always needed to ignore the bot message itself#
    if message.author == client.user:
        return
    
    if message.author.id == USER_ID['kkot'] :
        await message.channel.send("Jen stinks")
    if message.author == USER_ID['jonathan']:
        await message.channel.send("This is a targetted ad at you Jon")
    
    if message.content.startswith(COMMAND_PREFIX):
        try:
            command_name = message.content[len(COMMAND_PREFIX):].split()[0].lower()
            #parses the text after our prefix !text => text after
            command_func = commands.get(command_name)
            if command_func:
                await command_func(message)
        except discord.DiscordException as e:
            print(e)

help_commands = [
    "- All bot commands should start with ! and have no spaces after `!help` ",
    "- **help** : what you see is what you get",
    "- **tellmeajokke** : its empty",
    "- **getbook** : enter book details after command in any order (author title) `!getbook author title`"
]
@command('help')
async def helper(message):
    multi_line_msg = "\n".join(help_commands)
    await message.channel.send(multi_line_msg)

@command('tellmeajoke')
async def tell_joke(message):
    await message.channel.send(f"look in the mirror {message.author.mention}!")
# todo : HANDLE FILE LARGE EXCEPTION
@command('getbook')
async def get_book(message):
    url_path = "search_download/"
    requester = message.author
    #adding user state

    #message is the original bot command !getbook author title
    message_parsed = message.content.split()
    #ignore the first item
    search_string = ' '.join(message_parsed[1:])
    #requests post
    data = {"book_info" : search_string}
    try:
        response = requests.post('http://localhost:5000/search_download/' , json = data)
        #print(data)
    except:
        print("f response")

    ##### code below will be moved to "download" as pect later
    if response.status_code == 200:
        file_obj = discord_file_creation()
        try:
            await message.channel.send("File: ", file = file_obj)
        except discord.HTTPException as e:
            print(e)
        await message.channel.send(f"{message.author.mention}")
        requests.get('http://localhost:5000/cleanup')
    else:
        print("something went wrong")
        await message.channel.send("library is closed right now")
@command('getbook-adv')
async def getbook_adv(message):
    url_path = "search_download/"
    requester = message.author
    #adding user state
    if requester not in user_states:
        user_states[requester] = UserStates()
    state = user_states[requester]

    async def process_user_query():
        #message is the original bot command !getbook author title
        message_parsed = message.content.split()
        #ignore the first item
        search_string = ' '.join(message_parsed[1:])
        #requests post
        data = {"book_info" : search_string}
        try:
            response = requests.post('http://localhost:5000/search_download/' , json = data)
            #print(data)
        except:
            print("f response")

        if state.cancel_flag == True:
            await message.channel.send("Book request canned.")
            return
        
        unprocessed_response_payload= json.loads(response.content)
        state.book_options = unprocessed_response_payload['data'].split()
        my_msg = ""
        for idx,items in enumerate(state.book_options , start = 1):
            my_msg += f'{idx}. <{items}>\n'
        
        await message.channel.send(my_msg)

    state.task = client.loop.create_task(process_user_query())
    return
@command('cancel')
async def cancel(message):
    requester = message.author
    if requester in user_states and user_states[requester].task:
        user_states[requester].cancel_flag = True
    #await message.channel.send("Canned the current bot task.")

@command('shutdown')
async def kill_it(message):
    if message.author.id == creds.adminID:
        await message.channel.send("dead bot")
        await client.close()
    else:
        print(f'Stop it {message.author}.')
client.run(creds.myDiscordCreds)

