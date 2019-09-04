#!/usr/bin/env python3
import socket
import sys
import discord
from discord.ext import commands
import re

global client 
global channels


client = commands.Bot(command_prefix = '')
base_command = 'mudbot'

whitelist = open('whitelist.txt').read().splitlines()
the_help = open('help.txt').read()
channels = []

@client.event
async def on_ready():
    print('The Damned Thing Actually Started')


@client.event
async def on_message(message):
    if message.content.lower().startswith(base_command):
        work_with = message.content.lower().split(' ')
        if "help" == work_with[1]:
            await message.channel.send(the_help)

        if "create" == work_with[1] and "channel" == work_with[2]:
            if len(work_with) >= 3:
                da_name = work_with[3] + '-' + str(message.author.id)
                channeled = await message.guild.fetch_channels()
                if da_name in str(channeled):
                    await message.channel.send('That channel already exists, silly')
                else:
                    for categorie in message.guild.categories:
                        if str(categorie).lower() == mud_channel_category_name.lower():
                            await message.guild.create_text_channel(name = da_name, topic = 'Mud for ' + message.author.name, category = categorie)
            else:  
                await message.channel.send('Please insert a channel name')


async def respond(channel):
    print(str(channel))

#async def connection():

#async def modify_allowed():

mud_channel_category_name = 'muds'
bot_id = 
token = ''
client.run(token)
