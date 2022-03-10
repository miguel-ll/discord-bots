import discord
from discord.ext import commands
import musicbot

cogs = [musicbot]
BOT_TOKEN = "HERE GOES YOUR TOKEN"
client = commands.Bot(command_prefix='$', intents = discord.Intents.all())

@client.event
async def on_ready():
    print ("Bot is now online!")

for i in range(len(cogs)):
    cogs[i].setup(client)
    
client.run(BOT_TOKEN)
