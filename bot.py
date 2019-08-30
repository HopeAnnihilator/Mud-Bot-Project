#!/usr/bin/env python3
import socket
import sys
import discord
from discord.ext import commands

global command


client = commands.Bot(command_prefix = '')
command = 'mudbot'

claimed = 0
running = 0
login = ''
claim_user = ''
claim_channel = ''
target = ''
port = ''


@client.event
async def on_ready():
    print('The Damned Thing Actually Started')

@client.event
async def on_message(message):
    global claim_user, claim_channel, claimed, target, port, login, running, connect
    if message.content.lower().startswith(command.lower()): 
        if 'claim' in message.content and claimed != 1:
            if str(message.channel).startswith('Direct Message with ' + message.author.name):
                await message.channel.send('Unable to claim direct messages')
            else:
                claim_channel = message.channel.id
                await message.author.send('Please enter target server to connect beginning with ```target:```')
                claim_user = message.author.id
                claimed = 1
    elif claimed == 1 and running != 1 and message.author.id == claim_user and str(message.channel).startswith('Direct Message with ' + message.author.name):
        if message.content.startswith('target:'):
            target = message.content.replace(' ', '').split(':')
            try:
                await message.author.send(target[1] + ' is the current target')
                await message.author.send('Please enter port of server to connect beginning with ```port:```')
            except:
                await message.author.send('Sorry, I do not understand')
        elif message.content.startswith('port:'):
            port = message.content.replace(' ', '').split(':')
            try:
                await message.author.send(target[1] + ':' + port[1] + ' is the current server')
                await message.author.send('Please enter the login to mud beginning with ```login:```')
            except:
                await message.author.send('Sorry, I do not understand')
        elif message.content.startswith('login:'):
            login = message.content.split(':')
            await message.author.send('```' + login[1] + '```' + ' is the current login value, feel free to start mud with ```connect``` and login with ```login```')
    elif 'connect' in message.content and login and target and port and message.author.id == claim_user and message.channel.id == claim_channel:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        connect = s.connect((str(target[1]),int(port[1])))
        running = 1
        while True:
            try:
                banner = s.recv(8192).decode('utf-8','ignore')
                await message.channel.send(banner)
                print(banner)
            except socket.timeout:
                break
    elif running == 1 and message.author.id == claim_user and message.channel.id == claim_channel:
        if message.content.startswith('end'):
            running = 0
            claimed = 0
            s.close()
            target = ''
            port = ''
            login = ''
        elif message.content.startswith('login'):
            message = login + '\r\n'
            s.send(message.encode())
            result = s.recv(8192)
            print(result.decode())
        else:
            message = message.content + '\r\n'
            s.send(message.encode())
            result = s.recv(8192)
            print(result.decode())
            

bot_id = 610698989641400330
token = ''
client.run(token)
