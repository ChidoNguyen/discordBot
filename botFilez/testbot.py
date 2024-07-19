import discord
from discord.ext import tasks
import discordCreds as creds
import requests
import os
import json
import time,datetime
import concurrent.futures

from bot_command_subprocess import download_book , search_results , search_results_download
#bot permissions#
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents, heartbeat_timeout=60.0)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


#some housekeeping items and discord server specific for internal usage#
GUILD = "Janitors Guild"
API_ENDPOINT = { 
    'api' : "http://localhost:5000/",
    'cleanup' : "http://localhost:5000/cleanup/"
        }
ALLOWED_CHANNEL = ['im-testing-shit-ignore-me-chido','book-club']
USER_ID = {'kkot' : 705999688893071430, 'jonathan': 137004891360067584}

COMMAND_PREFIX = "!"
commands ={}
def command(name):
    def decorator(func):
        commands[name] = func
        return func
    return decorator
#user states
user_states = {}
class UserStates :
    def __init__(self):
        self.cancel_flag = False
        self.task = None
        self.book_options = []
        self.timestamp = None
        self.locked = False


def clean_up_users():
    current_time = datetime.now()
    for ppl in user_states:
        if ppl.timestamp != None and current_time - ppl.timestamp > datetime.timedelta(minutes=5):
            ppl.book_options = []
            ppl.timestamp = None

def isLocked(state):
    return state.locked
def userLock(state):
    state.locked = True
    return
def userUnlock(state):
    state.locked = False
    return
@tasks.loop(minutes = 5)
async def clean_up_tasks():
    clean_up_users()

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
    
    requester = message.author
    if requester not in user_states:
        user_states[requester] = UserStates()
    state = user_states[requester]
    if isLocked(state):
        await message.channel.send(f'One request at a time you greedy goblin. {requester.mention}')
        return
    #if not lock we lock
    userLock(state)
    if message.content.startswith(COMMAND_PREFIX):
        try:
            command_name = message.content[len(COMMAND_PREFIX):].split()[0].lower()
            #parses the text after our prefix !text => text after
            command_func = commands.get(command_name)
            if command_func:
                await command_func(message)
        except discord.DiscordException as e:
            print(e)
    userUnlock(state)

@command('thread_test')
async def thread_me(message):
    guild = discord.utils.get(client.guilds, name = GUILD)

    bot_member = guild.get_member(client.user.id)
    if not bot_member:
        print('Bot member not found in guild')
        return
    
    # # Check guild-wide permissions
    # if bot_member.guild_permissions.create_public_threads:
    #     print('The bot has the CREATE_PUBLIC_THREADS permission in this guild.')
    # else:
    #     print('The bot does not have the CREATE_PUBLIC_THREADS permission in this guild.')
    mythread = await message.channel.create_thread(name = message.content , auto_archive_duration = 60 , message = message)
    await mythread.send("something")

help_commands = [
    "- All bot commands should start with ! and have no spaces after `!help` ",
    "- **help** : what you see is what you get",
    "- **tellmeajoke** : its empty",
    "- **getbook** : enter book details after command in any order (author title) `!getbook author title`",
    "- **getbook-adv** : enter book details and get a list of links to pick from with `!pick` command" ,
    "- **pick** : enter number corresponding with link `!pick 3`"
]
@command('help')
async def helper(message):
    multi_line_msg = "\n".join(help_commands)
    await message.channel.send(multi_line_msg)

def single_task_limit(state):
    if state.task == None:
        return True
    return False

def task_clear(state):
    state.task = None

@command('getbook')
async def get_book(message):
    requester = message.author
    
    parsed_msg = message.content.split() #split by white spaces
    search_string = ' '.join(parsed_msg[1:])
    reply_thread = await message.channel.create_thread(
            name =f'{message.content}',
            message = message,
            auto_archive_duration = 60
        )

    await reply_thread.send('\U0001F50E')
    #hoping this unblocks the discord bot from timing out while waiting for it to finish
    future = executor.submit(download_book,search_string,requester)
    result = await client.loop.run_in_executor(None , future.result)
    if isinstance(result , tuple):
        #make thread
        file_obj , msg = result
        await reply_thread.send("File: ", file=file_obj)
        await reply_thread.send(msg)
        # await message.channel.send("File: ", file=file_obj)
        # await message.channel.send(msg)
    else:
        await message.channel.send(result)
    requests.get(API_ENDPOINT['cleanup'])

@command('getbook-adv')
async def getbook_adv(message):
    #url_path = "search_links/"
    requester = message.author
    #saving timestamp for future cleanup usage(?)
    state = user_states[requester]
    state.timestamp = datetime.datetime.now()

    parse_message = message.content.split()
    search_string = ' '.join(parse_message[1:])

    future = executor.submit(search_results,search_string,requester,state)
    state.task = await client.loop.run_in_executor(None, future.result)
    result = state.task
    await message.channel.send(result)

@command('pick')
async def pick_book(message):
    error_msg = {
        'invalid' : 'Too many or not enough parameters were given.' ,
        'invalid_choice' : 'Invalid link choice.',
        'invalid_num' : 'Please enter a number.',
        'task' : 'There is no book links attached to you.'
    }

    requester = message.author
    #check if user has ran a listings request yet
    try:
        state = user_states[requester]
    except:
        await message.channel.send(error_msg['task'])
        return 
    parsed_msg = message.content.split()

    '''
    no task , not enough params , not a valid pick
    '''
    try:
        an_int = int(parsed_msg[1])
    except:
        await message.channel.send(error_msg['invalid_num'])
        return
    if not state.task :
        await message.channel.send(error_msg['task'])
    elif len(parsed_msg) != 2: # we want botcommand at 1 and 2 is the pick
        await message.channel.send(error_msg['invalid'])
    elif (0 >= int(parsed_msg[1]) or int(parsed_msg[1]) > len(state.book_options)):
        await message.channel.send(error_msg['invalid_choice'])
    else:
        await message.channel.send("Sit tight.")
        user_choice = int(parsed_msg[-1]) - 1 # convert to 0 index
        future = executor.submit(search_results_download,user_choice,requester,state)
        result = await client.loop.run_in_executor(None, future.result)
        if isinstance(result, tuple):
            f , msg = result
            await message.channel.send("File: ", file=f)
            await message.channel.send(msg)
            state.task = None
            state.book_options = []
        else:
            await message.channel.send(result)
    requests.get(API_ENDPOINT['cleanup'])

@command('cancel')
async def cancel(message):
    requester = message.author
    if requester in user_states and user_states[requester].task:
        user_states[requester].cancel_flag = True
    #await message.channel.send("Canned the current bot task.")
@command('tellmeajoke')
async def tell_joke(message):
    await message.channel.send(f"look in the mirror {message.author.mention}!")
@command('shutdown')
async def kill_it(message):
    if message.author.id == creds.adminID:
        await message.channel.send("dead bot")
        await client.close()
    else:
        print(f'Stop it {message.author}.')
        await message.channel.send(f'Stop it {message.author}')

def run_bot():       
    client.run(creds.myDiscordCreds)

if __name__  ==  '__main__':
    run_bot()
