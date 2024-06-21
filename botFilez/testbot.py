import discord
import discordCreds as creds



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

GUILD = "Janitors Guild"

ALLOWED_CHANNEL = ['im-testing-shit-ignore-me-chido']
########bot command decorator setups ########

COMMAND_PREFIX = "!"
commands ={}
def command(name):
    def decorator(func):
        commands[name] = func
        return func
    return decorator

##### * * ###################

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
    if message.author == 'kkot.':
        await message.channel.send("jen stinks")
    if message.author == 'fungasm.':
        await message.channel.send("testing")
    if message.content.startswith(COMMAND_PREFIX):
        try:
            command_name = message.content[len(COMMAND_PREFIX):].split()[0]
            #parses the text after our prefix !text => text after
            command_func = commands.get(command_name)
            if command_func:
                await command_func(message)
        except:
            await message.channel.send(f'Stop it {message.author}')

    

@command('tellmeajoke')
async def tell_joke(message):
    await message.channel.send("no")


client.run(creds.myDiscordCreds)

