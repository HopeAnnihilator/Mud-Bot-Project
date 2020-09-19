#!/usr/bin/env python3
import socket
import sys
import discord
from discord.ext import commands
import re

global command


client = commands.Bot(command_prefix = '')
command = 'mudbot'

whitelist = open('whitelist.txt').read().splitlines()

claimed = 0
running = 0
claim_user = ''
claim_channel = ''
target = ''
port = 0
login = ''
allowed_users = []

def remove_claim():
    global claimed, running, claim_user, claim_channel, target, port, login, allowed_users
    claimed = 0
    running = 0
    claim_user = ''
    claim_channel = ''
    target = ''
    port = 0
    login = ''
    allowed_users = []

@client.event
async def on_ready():
    print('The Damned Thing Actually Started')

@client.event
async def on_message(message):
    global claim_user, claim_channel, claimed, target, port, login, running, connect, s, allowed_users
    if message.content.lower().startswith(command.lower()):
        if 'remove_claim' in message.content and claimed == 1 and (message.author.id == claim_user or "name='staff'" in str(message.author.roles).lower()):
            remove_claim()
            await message.channel.send('Claim has been removed')
        elif 'claim' in message.content and claimed != 1:
            if str(message.channel).startswith('Direct Message with ' + message.author.name):
                await message.channel.send('Unable to claim direct messages')
            else:
                claim_channel = message.channel.id
                await message.author.send('Please enter target server to connect beginning with ```target:```')
                claim_user = message.author.id
                claimed = 1



    elif claimed == 1 and running != 1 and message.author.id == claim_user and str(message.channel).startswith('Direct Message with ' + message.author.name):
        da_dum = message.content.lower()
        if da_dum.startswith('target:'):
            target = message.content.replace(' ', '').split(':')
            
            try:
                if target [1] in whitelist:
                    await message.author.send(target[1] + ' is the current target')
                    await message.author.send('Please enter port of server to connect beginning with ```port:```')
                else:
                    await message.author.send("That target is not allowed")
            except:
                await message.author.send('Sorry, I do not understand')
        elif da_dum.startswith('port:'):
            port = message.content.replace(' ', '').split(':')
            try:
                await message.author.send(target[1] + ':' + port[1] + ' is the current server')
                await message.author.send('Please enter the login to mud beginning with ```login:```')
            except:
                await message.author.send('Sorry, I do not understand')
        elif da_dum.startswith('login:'):
            login = message.content.split(':')
            await message.author.send('```' + login[1] + '```' + ' is the current login value, feel free to start mud with ```connect``` and login with ```session login``` logout with ```session end```')
    elif message.content.lower().startswith('connect') and login and target and port and message.author.id == claim_user and message.channel.id == claim_channel and running != 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        connect = s.connect((str(target[1]),int(port[1])))
        running = 1
        while True:
            try:
                banner = s.recv(8192).decode('utf-8','ignore')
                banner = re.sub(r".{0,3}m", '', str(banner))
                banner = re.sub(r"VFE.{1}", '', str(banner))

                if banner:
                    await message.channel.send('```' + banner + '```')
                    print(banner)
            except socket.timeout:
                break
    elif running == 1 and (message.author.id == claim_user or str(message.author.id) in allowed_users) and message.channel.id == claim_channel and message.author.id != bot_id:
        if message.content.startswith('session'):
            if "end" in message.content:
                remove_claim()
                await message.channel.send("Session Ended")
                s.close()
            elif "login" in message.content:
                kudo = str(login[1]) + '\r\n'
                s.send(kudo.encode())
                while True:
                    try:
                        banner = s.recv(8192)
                        print(str(banner))
                        banner = banner.decode('utf-8','ignore')
                        banner = re.sub(r".{0,3}m", '', str(banner))
                        banner = re.sub(r".{0,1}38;5;208m", '', str(banner))
                        banner = re.sub(r"\r\r\n", '\r\n', str(banner))
                        if banner:
                            await message.channel.send('```' + banner + '```')
                            print(banner)
                    except socket.timeout:
                        break
            elif "allow" in message.content:
                if message.mentions:
                    print(str(message.mentions))
                    print(str(message.mentions)[12:30])
                    allowed_users.append(str(message.mentions)[12:30])
                    await message.channel.send(str(message.mentions)[12:30] + ' added to allowed users')
                else:
                    await message.channel.send('Please mention a user')
        elif message.content.startswith('%'):
            print(message.content)
        else:
            kudo = message.content + '\r\n'
            s.send(kudo.encode())
            while True:
                try:
                    banner = s.recv(8192)
                    print(str(banner))
                    banner = banner.decode('utf-8','ignore')
                    banner = re.sub(r".{0,3}m", '', str(banner))
                    banner = re.sub(r".{0,1}38;5;208m", '', str(banner))
                    banner = re.sub(r"\r\r\n", '\r\n', str(banner))
                    if banner:
                        await message.channel.send('```' + banner + '```')
                        print(banner)
                except socket.timeout:
                    break
            

bot_id = 
token = ''
client.run(token)
test to delete later
