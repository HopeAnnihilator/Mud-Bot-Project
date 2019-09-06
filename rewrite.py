#!/usr/bin/env python3
import socket
import sys
import discord
from discord.ext import commands
import re
import asyncio
import time

global client 
global channels
global whitelist
global running 
global claimed, claim_user, claim_channel, allowed_users


client = commands.Bot(command_prefix = '')
base_command = 'mudbot'

whitelist = open('whitelist.txt').read().splitlines()
the_help = open('help.txt').read()
channels = []

claimed = False
claim_user = 0
claim_channel = 0
running = False
server = ''
port = 0
allowed_users = []

@client.event
async def on_ready():
    print('The Damned Thing Actually Started')


@client.event
async def on_message(message):
    if message.content.lower().startswith(base_command):
        work_with = message.content.lower().split(' ')
        if "help" == work_with[1]:
            await message.channel.send(the_help)
        elif "create" == work_with[1] and "channel" == work_with[2] and str(type(message.channel)) == "<class 'discord.channel.TextChannel'>":
            if len(work_with) >= 4:
                da_name = work_with[3] + '-' + str(message.author.id)
                channeled = await message.guild.fetch_channels()
                if da_name in str(channeled):
                    await message.channel.send('That channel already exists, silly')
                elif (str(message.author.id)) in str(channeled):
                    await message.channel.send('You have already created a channel')
                else:
                    for categorie in message.guild.categories:
                        if str(categorie).lower() == mud_channel_category_name.lower():
                            await message.guild.create_text_channel(name = da_name, topic = 'Mud for ' + message.author.name, category = categorie, slowmode_delay = 1)
            else:  
                await message.channel.send('Please insert a channel name')
        elif "claim" == work_with[1]:
            if str(type(message.channel)) == "<class 'discord.channel.TextChannel'>":
                global claimed, claim_user, claim_channel, da_channel
                if claimed and message.author.id != claim_user:
                    await message.channel.send('The bot is already claimed')
                elif claimed and message.author.id == claim_user:
                    await message.channel.send('You already have a claim')
                else:
                    claim_channel = message.channel.id
                    await message.author.send('Please message the target server in the form ```target.server:port```')
                    claim_user = message.author.id
                    claimed = True
                    da_channel = message.channel
            else:
                await message.channel.send('Cannot claim this channel')
        elif "remove" == work_with[1] and str(type(message.channel)) == "<class 'discord.channel.TextChannel'>":
            if "claim" == work_with[2]:
                if (message.author.id == claim_user or "name='staff'" in str(message.author.roles).lower()):
                    if claimed:
                        await remove_claim()
                    else:
                        await message.channel.send('There are no active claims')
                else:
                    await message.channel.send('You are unable to remove claims')
            elif "channel" == work_with[2]:
                if "name='staff'" in str(message.author.roles).lower():
                    if len(work_with) >= 4 and message.author.id == message.guild.owner.id:
                        if work_with[3] == "all":
                            for channel in message.guild.channels:
                                await channel.delete()
                        else:
                            await message.channel.send('Sorry, no comprendo')                            
                    await message.channel.delete()
                elif str(message.author.id) in message.channel.name:
                    await message.channel.delete()
                else:
                    await message.channel.send('Fuck off, you cant do that')
        elif "connect" == work_with[1] and claimed and message.channel.id == claim_channel and message.author.id == claim_user and not running:
            global server, port
            await message.channel.send('Attempting to connect')
            await mudbot_connect(server, port)  
        elif "secret" == work_with[1] and message.channel.id == claim_channel and message.author.id == claim_user:
            await send_secret()   
        elif "allow" == work_with[1] and message.author.id == claim_user and claimed:
            if message.mentions:
                allowed_users.append(str(message.mentions)[12:30])
                await message.channel.send(str(message.mentions)[12:30] + ' added to allowed users')
            else:
                await message.channel.send('Please mention a user')
        elif "banish" == work_with[1] and (message.author.id == claim_user or "name='staff'" in str(message.author.roles).lower()) and claimed:
            if message.mentions:
                if str(message.mentions)[12:30] in allowed_users and str(message.mentions)[12:30] != str(claim_user):
                    allowed_users.remove(str(message.mentions)[12:30])
                    await message.channel.send(str(message.mentions)[12:30] + ' removed from allowed users')
                else:
                    await message.channe.send('Unable to remove ' + str(message.mentions)[12:30])
            else:
                await message.channel.send('Please mention a user')
    elif str(type(message.channel)).lower() == "<class 'discord.channel.dmchannel'>" and message.author.id != bot_id:
        if message.author.id == claim_user:
            work_with = message.content.lower().split(':')
            if work_with[0] == "secret":
                if len(work_with) >= 2:
                    if work_with[1]:
                        global secret
                        secret = work_with[1]
                        await message.channel.send("Your secret is currently set to ```" + secret + '```')
                    else:
                        await message.channel.send("Please add a secret")
                else:
                    await message.channel.send("Please add a secret")
            elif len(work_with) >= 2:
                try:
                    int(work_with[1])
                    if work_with[0] in whitelist:
                        await message.channel.send('The current target is```' + work_with[0] + ':' + str(work_with[1]) + '```')
                        await message.channel.send('If you would like to share a secret such as login info you can submit information such as this using ```secret: connect username password``` which can then be called upon in the claimed channel using ```mudbot secret``` instead of typing this information for everyone to see, this can be editted by dming the bot any time you have the claim by beggining the dm with ```secret:```')
                        await message.channel.send('While choosing a secret is optional, you may now start the bot by typing ```mudbot connect``` in the channel you claimed')
                        server = str(work_with[0])
                        port = int(work_with[1])
                    else:
                        await message.channel.send('Sorry, that server is not in the whitelist')
                except ValueError:
                    await message.channel.send('I do not understand, remember ports must be integers')
            else:
                await message.channel.send('Do you know what you are trying to do?')
        elif message.author.id != bot_id:
            await message.channel.send('I am not accepting dms at this time')
    elif message.channel.id == claim_channel and (message.author.id == claim_user or str(message.author.id) in allowed_users) and running and not message.content.startswith('%'):
        kudo = message.content + '\r\n'
        s.send(kudo.encode())


async def mudbot_connect(server, port):
    global s, running, connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    print(server)
    print(port)
    connect = s.connect((str(server), int(port)))
    running = True
    await receive_info()


async def receive_info():
    while True:
        try:
            banner = s.recv(8192)
            print(str(banner))
            banner = banner.decode('utf-8','ignore')
            banner = re.sub(r".{0,3}m", '', str(banner))
            banner = re.sub(r".{0,1}38;5;208m", '', str(banner))
            banner = re.sub(r"\r\r\n", '\r\n', str(banner))
            banner = re.sub(r"VFE.{1}", '', str(banner))
            if banner:
                await da_channel.send('```' + banner + '```')
                print(banner)
        except socket.timeout:
            break
    await asyncio.sleep(0.1)
    await receive_info()
                
async def send_secret():
    global secret
    if secret:
        kudo = secret + '\r\n'
        s.send(kudo.encode())
        secret = ''

async def remove_claim():
    global claimed, claim_user, claim_channel, running, server, port
    claimed = False
    claim_user = 0
    claim_channel = 0
    running = False
    server = ''
    port = 0
    s.close()

mud_channel_category_name = 'muds'
bot_id = 
token = ''
client.run(token)
