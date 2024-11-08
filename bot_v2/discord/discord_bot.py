import discord
from collections import defaultdict
from user_states import UserStates
from bot_config import USER_KEY





#discord client permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
client = discord.Client(intents=intents)

COMMAND_PREFIX = "!"

'''
commands (dict) stores bot-commands implemented
'''
commands = {}
def command(name):
    def decorator(func):
        commands[name] = func
        return func
    return decorator

'''
UserStates : for house keeping purposes to limit or expand users bot usage
'''
user_states = defaultdict(UserStates)


@client.event
async def on_ready():
    server_name = discord.utils.get(client.guilds)
    print(f'Logged in as {client.user} in {server_name}.')

'''
event.on_message(): listening for when bot commands are invoked by users
'''
@client.event
async def on_message(message):
    if message.author == client.user: #ignores bots own messages
        return
    
    requester = message.author
    user = user_states[requester]
    try:
        if message.content.startswith(COMMAND_PREFIX):
            no_prefix = message.content[len(COMMAND_PREFIX):]
            message_word_content = no_prefix.split()
            command_name = message_word_content[0].lower()

            if command_name not in commands:
                await message.channel.send(f'Command does not exist.')
                return
            
            command_function = commands.get(command_name)
            print(f'{requester} : {command_name}')
            if command_name in ['admin' , 'cancel']: #bypass user lock outs
                await command_function(message)
            else:
                if user.isLocked():
                    await message.channel.send(f'One request at a time you greedy goblin. {requester.mention}')
                    return
                user.lock()
                await command_function(message)
                user.unlock()
    except discord.DiscordException as e:
        print(f'Error: {e}')
        print(f'{requester} : {command_name} failed.')

@command('help')
async def help_msg(message):
    help_commands = [
        "- All bot commands should start with ! `!help` ",
        "- **help** : what you see is what you get",
        "- **tellmeajoke** : its empty",
        "- **getbook** : enter book details after command in any order (author title) `!getbook author title`",
        "- **getbook-adv** : enter book details and get a list of links to pick from with `!pick` command" ,
        "- **pick** : enter number corresponding with link `!pick 3`"
    ]
    multi_line_msg = "\n".join(help_commands)
    await message.channel.send(multi_line_msg)

@command('getbook')
async def get_book(message):
    requester = message.author
    msg_content = message.content.split()
    
    #create discord message thread for server clarity
    reply_thread = await message.channel.create_thread(
        name = f'{requester} book request thread' ,
    )
    if len(msg_content) < 2:
        await reply_thread.send("Missing book details.")
        return
    
    search_phrase = ' '.join(msg_content[1:]) #omit bot command 
    await reply_thread.send('\U0001F50E')
    # @TODO spin up our scripts to get the book and upload to server
    return

@command('getbook-adv')
async def get_book_adv(message):
    requester = message.author
    user = user_states[requester]
    if user.pick_options:
        await message.channel.send(f'Another getbook-adv request in progress. Either !pick or !cancel.')
        return
    search_string = ' '.join(message.content.split()[1:])
    reply_thread = await message.create_thread(
        name = f'{requester} book request thread.',
    )
    await reply_thread.send(f'Working on it.')
    # @TODO spin up script to do work and print list of url we get
    print(type(reply_thread))
    return

@command('pick')
async def pick_url(message):
    return



def bot_start():
    try:
        client.run(USER_KEY)
    except Exception as e:
        print(f'Bot initilization failed.')
        print(e)

if __name__ == '__main__':
    bot_start()