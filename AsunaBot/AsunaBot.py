from discord.ext import commands
from bs4 import BeautifulSoup
from random import randrange

import random
import requests
import logging
import discord
import bs4
import config
import re

DESCRIPTION = ''' A discord bot

Written by: Knotts'''

logging.basicConfig(level=logging.INFO)

AsunaBot = commands.Bot(command_prefix='!', description=DESCRIPTION)
client = discord.Client()

if not discord.opus.is_loaded():
    discord.opus.load_opus('/mnt/c/Projects/opusfile/libopus.so')

@AsunaBot.event
async def on_ready():
    print('Logged in as')
    print(AsunaBot.user.name)
    print(AsunaBot.user.id)
    print('------')

@AsunaBot.command()
async def feelsbadman(*args):
    await AsunaBot.say('https://imgur.com/aSVjtu7')

# Posts link to op.gg profile of 'ign'
@AsunaBot.command()
async def opgg(*, ign: str):
    pattern = re.compile(r'\s+')
    ign = re.sub(pattern, '+', ign)
    await AsunaBot.say('http://na.op.gg/summoner/userName={}'.format(ign))

# Posts a random image of 'name' from zerochan.net
@AsunaBot.command()
async def showme(*, name: str):
    urlArray = []
    pattern = re.compile(r'\s+')
    name = re.sub(pattern, '+', name)
    url = 'https://www.zerochan.net/{}'.format(name)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for link in soup.find_all('a'):
        if 'static' in str(link.get('href')):
            urlArray.append(str(link.get('href')))
    index = randrange(0, len(urlArray))
    imageUrl = urlArray[index]
    urlArray.pop(index)
    await AsunaBot.say(imageUrl)

# Return MAL link for the anime 'title'
@AsunaBot.command()
async def mal(*, title: str):
    url = 'https://myanimelist.net/search/all?q={}'.format(title)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    pattern = re.compile(r'\s+')
    title = (re.sub(pattern, '_', title))
    for link in soup.find_all('a'):
        if re.search(r'\/anime\/(\d*)\/' + title + '(?![\/_])', str(link.get('href')), re.IGNORECASE):
            await AsunaBot.say(link.get('href'))
            return

@AsunaBot.command()
async def bm(*, title:str):
    url = 'https://osu.ppy.sh/p/beatmaplist?q={}'.format(title)
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for link in soup.find_all('a'):
        if '/s/' in str(link.get('href')):
            # print(link.get('href'))
            return

AsunaBot.run(config.token)
