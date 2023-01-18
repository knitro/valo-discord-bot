import discord
import constants
 
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!val patch"):

        command_items = message.content.split(" ") # Index 0: !val, 1: patch, 2+...
        val_version = "1.0"
        if len(command_items) <= 2:
            val_version = await get_latest_val_version()
        else:
            val_version = command_items[2]

        patch_notes_url = await get_latest_patch_notes()       
        message_contents = "The latest patch notes for version " + val_version + " is below: \n" + patch_notes_url
        await message.channel.send(message_contents)
        await get_latest_patch_notes()

    elif message.content.startswith('hi knitro'):
        await message.channel.send('Hello!')

async def get_latest_patch_notes():
    version = await get_latest_val_version()
    version_url_safe = convert_number_url_friendly(version)
    return "https://playvalorant.com/en-us/news/game-updates/valorant-patch-notes-" + version_url_safe
 
async def get_latest_val_version():
    return "6.0"

def convert_number_url_friendly(value):
    return value.replace(".", "-")

client.run(constants.DISCORD_API_KEY)