# pip install dismusic==1.0.1
# pip install discord-custom-help
from discord.ext import commands

bot = commands.Bot(command_prefix='?')
BOT_TOKEN = "HERE GOES THE TOKEN"

bot.lava_nodes = [
    {
        'host': 'lava.link',
        'port': 80,
        'rest_uri': f'http://lava.link:80',
        'identifier': 'MAIN',
		'password': 'anything',
		'region': 'singapore'
	}

]

@bot.event

async def on_ready():
    print('Bot is ready')
    bot.load_extension('dismusic')
    bot.load_extension('dch')
	
bot.run(BOT_TOKEN)
