import discord
from discord.ext import tasks
import discordCreds as creds
import requests
import os
import json
import time,datetime
import concurrent.futures
import random

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
ALLOWED_CHANNEL = [
    1265781830683197501 , #test channel
    877784047722569728 # book club
]
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
    #restrict channels only listen for commands from designated channels
    #if message.channel.id not in ALLOWED_CHANNEL:
    #   return
    #if pick need to verify thread is in allowed cc
    
    if message.channel.id not in ALLOWED_CHANNEL and (not isinstance(message.channel,discord.Thread) or message.channel.parent_id not in ALLOWED_CHANNEL):
        return
    #track tasks/requests from specific users
    requester = message.author
    if requester not in user_states:
        user_states[requester] = UserStates()
    state = user_states[requester]
    try:
        if message.content.startswith(COMMAND_PREFIX):
            # TODO: use a more clean approach via discord bot predicates
            # flow check.... admin should be able to bypass all
            #we get the message content ignoring the command prefix via len
            #split it for spaces and grab first word in the split array via [0]
            command_name = message.content[len(COMMAND_PREFIX):].split()[0].lower()
            command_function = commands.get(command_name)
            print(f'{requester} : {command_name}')
            if not command_function:
                await message.channel.send(f"Command does not exist.")
            elif command_name == 'admin':
                await command_function(message)
            elif command_name == 'cancel':
                await command_function(message)
            else:
                if isLocked(state):
                    await message.channel.send(f'One request at a time you greedy goblin. {requester.mention}')
                    return
                userLock(state)
                await command_function(message)
                userUnlock(state)
    except discord.DiscordException as e:
        print(f'Something went wrong error : {e}')
        await message.channel.send(f'Something broke , abort mission.')
    ''' 10/28/2024 working
    if message.content.startswith(COMMAND_PREFIX):
        if isLocked(state):
            await message.channel.send(f'One request at a time you greedy goblin. {requester.mention}')
            return
    #if not lock we lock
        userLock(state)
        try:
            command_name = message.content[len(COMMAND_PREFIX):].split()[0].lower()
            #parses the text after our prefix !text => text after
            print(f'{requester} : {command_name}')
            command_func = commands.get(command_name)
            if command_func:
                await command_func(message)
        except discord.DiscordException as e:
            print(e)
        userUnlock(state)
    '''


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
            name =f'{message.author} book request thread.',
            message = message,
            auto_archive_duration = 60
        )
    if len(parsed_msg) < 2:
        await reply_thread.send("Missing book details.")
        return
    #some message to let users know bot is doing something
    await reply_thread.send('\U0001F50E')

    #future/exec helps prevent discord heartbeat timeout
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
        await reply_thread.send(result)

@command('getbook-adv')
async def getbook_adv(message):
    #url_path = "search_links/"
    requester = message.author
    #saving timestamp for future cleanup usage(?)
    state = user_states[requester]
    state.timestamp = datetime.datetime.now()

    parse_message = message.content.split()
    search_string = ' '.join(parse_message[1:])

    reply_thread = await message.create_thread(
        name =f'{message.author} book request thread.',
        #message = message, this is needed if we message.channel.create_thread 
        # above creates thread in channel from message we pass
        auto_archive_duration = 60
    )
    tmp = await reply_thread.send("Working on it.")
    """ try:
        print(type(message),type(reply_thread),message.thread.id)
    except discord.ClientException as e:
        print(e)
    except discord.DiscordException as f:
        print(f)
    return """
    future = executor.submit(search_results,search_string,requester,state)
    state.task = await client.loop.run_in_executor(None, future.result)
    result = state.task
    #await message.channel.send(result)
    
    await reply_thread.send(result)

@command('pick')
async def pick_book(message):#
    error_msg = {
        'invalid' : 'Too many or not enough parameters were given.' ,
        'invalid_choice' : 'Invalid link choice.',
        'invalid_num' : 'Please enter a number.',
        'task' : 'There is no book links attached to you.'
    }
    reply_thread = message.channel
    requester = message.author
    #### error flow###
    #no task -> wrong channel -> invalid inputs
    if requester not in user_states or user_states[requester].task == None:
        await message.channel.send(f"{error_msg['task']} Run !getbook-adv")
        return
    elif not isinstance(reply_thread, discord.Thread):
        await message.delete()
        await message.channel.send(f'Pick in the book request thread. {requester.mention}' , delete_after = 5)
        return
    
    #check if user has ran a listings request yet
    # try:
    state = user_states[requester]
    # except:
    #     await reply_thread.send(error_msg['task'])
    #     return 
    parsed_msg = message.content.split()

    '''
    no task , not enough params , not a valid pick
    '''
    try:
        an_int = int(parsed_msg[1])
    except:
        await reply_thread.send(error_msg['invalid_num'])
        return
    # if not state.task :
    #     await reply_thread.send(error_msg['task'])
    if len(parsed_msg) != 2: # we want botcommand at 1 and 2 is the pick
        await reply_thread.send(error_msg['invalid'])
    elif (0 >= int(parsed_msg[1]) or int(parsed_msg[1]) > len(state.book_options)):
        await reply_thread.send(error_msg['invalid_choice'])
    else:
        await reply_thread.send("Sit tight.")
        user_choice = int(parsed_msg[-1]) - 1 # convert to 0 index
        future = executor.submit(search_results_download,user_choice,requester,state)
        result = await client.loop.run_in_executor(None, future.result)
        if isinstance(result, tuple):
            f , msg = result
            await reply_thread.send("File: ", file=f)
            await reply_thread.send(msg)
            state.task = None
            state.book_options = []
        else:
            await reply_thread.send(result)

@command('cancel')
async def cancel(message):
    requester = message.author
    if requester in user_states and user_states[requester].task:
        user_states[requester].cancel_flag = True
    #await message.channel.send("Canned the current bot task.")
@command('roll')
async def roll(message):
    bot , top = 0 , 100
    rng = random.randint(bot,top)
    if rng < 80 :
        await message.channel.send(f"Jon's unlucky touch got you {rng}.")
    else:
        await message.channel.send(f"Jon's lucky touch got you {rng}.")
    return

@command('tellmeajoke')
async def tell_joke(message):
    await message.channel.send(f"look in the mirror {message.author.mention}!")
@command('admin')
async def admin_panel(message):
    await message.channel.send(f'my brain hurts')
@command('cleanup')
async def thread_clean(message):
    if message.author.id != creds.adminID:
        await message.channel.send(f"You don't have janitor clearance.")
        return
    
    #source
    request_channel = message.channel.id
    target_cc = client.get_channel(request_channel)
    for items in target_cc.threads:
        await items.delete()
    await message.delete()
    await message.channel.send("Threads deleted.")
    print(f'Cleaning up threads.')
    return
@command('admin-purge')
async def hard_purge(message):
    if message.author.id != creds.adminID:
        await message.channel.send(f"Tsk tsk tsk you're not an admin.")
        return
    request_channel = message.channel.id
    await client.get_channel(request_channel).purge(limit = 10)
    print('Purged a batch of messages.')
    return

@command('admin-shutdown')
async def kill_it(message):
    if message.author.id == creds.adminID:
        await message.channel.send("dead bot")
        await client.close()
    else:
        print(f'Stop it {message.author}.')
        await message.channel.send(f'Stop it {message.author}')

def run_bot(): 
    try:
        response = requests.get(API_ENDPOINT['api'] + "online")
        client.run(creds.myDiscordCreds)
    except Exception as e:
        print(e , '\n')
        print("Webserver is not active.")

if __name__  ==  '__main__':
    run_bot()
