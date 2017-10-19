# The main file for AsunaBot

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
import xml.etree.cElementTree as ET

from animethemes import findAnimeOpening, findAnimeEnding, randomIrlPost

DESCRIPTION = ''' A discord bot

Written by: Knotts'''

# logging.basicConfig(level=logging.INFO)

AsunaBot = ''

print('Logging onto AsunaBot...')
AsunaBot = commands.Bot(command_prefix='!', description=DESCRIPTION)
client = discord.Client()
print('Setup complete')
print('-------------------------')

if not discord.opus.is_loaded():
    discord.opus.load_opus('/mnt/c/Projects/opusfile/libopus.so')

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

# Return MAL link for the anime 'title' by webscraping
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

# Return MAL link for the anime 'title' using myanimelist.net's api
@AsunaBot.command()
async def mal2(*, title: str):
    url = 'https://myanimelist.net/anime/'
    pattern = re.compile(r'\s+')
    title = re.sub(pattern, '+', title)
    mal = requests.Session()
    request = mal.get('https://myanimelist.net/api/anime/search.xml?q={}'.format(title), auth=(config.username, config.password))
    mal.close()
    request = ET.fromstring(convertXML(request.text))

    anime = request.find('./entry')
    title = anime.find('title').text
    animeId = anime.find('id').text
    title = re.sub(pattern, '_', title)
    url += animeId + '/' + title

    await AsunaBot.say(url)

# The bot will comment with a mp4 link of an OP from /r/AnimeThemes for a given anime
@AsunaBot.command()
async def op(*, titlez: str):
    openings = findAnimeOpening(titlez)
    # Most likely an invalid anime title
    if(openings == -1): 
        await AsunaBot.say('I couldn\'t find any openings for this anime you potato <:PunOko:370486584153473024>')
        return

    # Prevent the bot from spamming too many links because of bad requests
    if(len(openings) > 8):
        await AsunaBot.say('This request has too many links')
        return

    await AsunaBot.say('<:VoHiYo:370487040380239872> Here are the opening(s) for \"' + titlez + '\" <:VoHiYo:370487040380239872>')
    for anime in openings:
        if('reddit' not in anime.url):
            await AsunaBot.say(anime.title)
            await AsunaBot.say(anime.url)

    await AsunaBot.say('<:TehePelo:370494286707425280> Not what you were looking for? Check the title of the anime and try again! <:TehePelo:370494286707425280>')

# The bot will comment with a mp4 link of an ED from /r/AnimeThemes for a given anime
@AsunaBot.command()
async def ed(*, title: str):
    endings = findAnimeEnding(title)
    if(endings == -1):
        await AsunaBot.say('I couldn\'t find any endings for this anime you ape <:PunOko:370486584153473024>')
        return

    # Prevent the bot from spamming too many links because of bad requests
    if(len(openings) > 8):
        await AsunaBot.say('This request has too many links')
        return

    await AsunaBot.say('<:VoHiYo:370487040380239872> Here are the ending(s) for \"' + title + '\" <:VoHiYo:370487040380239872>')
    for anime in endings:
        if('reddit' not in anime.url):
            await AsunaBot.say(anime.title)
            await AsunaBot.say(anime.url)

    await AsunaBot.say('<:TehePelo:370494286707425280> Not what you were looking for? Check the title of the anime and try again! <:TehePelo:370494286707425280>')

# Retrieves a random post from /r/anime_irl
@AsunaBot.command()
async def me_irl():
    url = randomIrlPost()
    await AsunaBot.say(url)

# taken from https://github.com/Nihilate/Roboragi/blob/master/roboragi/MAL.py
def convertXML(text):
    import html.parser

    text = text.replace('&Eacute;', 'É').replace('&times;', 'x').replace('&rsquo;', "'").replace('&lsquo;', "'").replace('&hellip', '...').replace('&le', '<').replace('<;', '; ').replace('&hearts;', '♥').replace('&mdash;', '-')
    text = text.replace('&eacute;', 'é').replace('&ndash;', '-').replace('&Aacute;', 'Á').replace('&acute;', 'à').replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&Oslash;', 'Ø').replace('&frac12;', '½').replace('&infin;', '∞')
    text = text.replace('&agrave;', 'à').replace('&egrave;', 'è').replace('&dagger;', '†').replace('&sup2;', '²').replace('&#039;', "'")

    return text

    text=html.parser.HTMLParser().unescape(text)
    return html.parser.HTMLParser().unescape(text)
  
AsunaBot.run(config.token)
