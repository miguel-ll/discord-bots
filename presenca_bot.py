import discord
from discord.ext import commands
import datetime
import os.path
import re

BOT_TOKEN = ""

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")
intents.members = True

def get_date():
    x = str(datetime.datetime.now())
    x = x.split()[0]
    x = x.split('-')
    return f"{x[2]}-{x[1]}-{x[0]}"

file_path = f"{get_date()}.txt"

def create_db(num, t):
    import sqlite3
    conn = sqlite3.connect('lista_presenca.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE presenca (
                     numero_matricula integer,
                     turma text,
                     data text
        )""")
    except:
        pass
    c.execute("INSERT INTO presenca VALUES (?, ?, ?)", (num, t, get_date()))
    conn.commit()
    conn.close()

def create_file(text):
    if os.path.exists(file_path):
        with open(file_path, 'a') as fp:
            fp.write(f"\n{text}")
    else:
        with open(file_path, 'w') as fp:
            fp.write(str(text))

@client.command(pass_context=True)
async def presenca(ctx, msg=None):
    username = re.sub('\#.*', '', str(ctx.author))
    if len(msg) < 11:
        await ctx.send("Erro. Digite uma presença válida.")
        return
    if msg is not None:
        try:
            create_db(int(msg), str(ctx.message.channel))
            create_file(f"{msg} {ctx.message.channel}")
            await ctx.message.delete()
            await ctx.send(f"Presença registrada para {username}!")
        except:
            await ctx.send("Erro. Digite uma presença válida.")
    else:
        await ctx.send(f"{ctx.message.author.mention}, digite !presenca e o número da matrícula!\nExemplo: !presenca 2021008079")

@client.command(pass_context=True)
async def get(ctx):
    global file_path
    f = open(file_path, 'r')
    fc = f.read()
    f.close()
    emb_msg = discord.Embed(title=f"Presenças do dia {get_date()}:", description=fc)
    guild_owner = client.get_user(int(ctx.guild.owner.id))
    await guild_owner.send(embed=emb_msg)

@client.event
async def on_ready():
    print("The bot is now online!")

client.run(BOT_TOKEN)
