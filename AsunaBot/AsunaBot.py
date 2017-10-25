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

from animethemes import findAnimeOpening, findAnimeEnding, randomPost

DESCRIPTION = ''' A discord bot


Written by: Knotts'''

startup_extensions = ['Music']

# logging.basicConfig(level=logging.INFO)

print('Logging onto bot...')
bot = commands.Bot(command_prefix='~', description=DESCRIPTION)
bot.load_extension('Music')
client = discord.Client()
print('Setup complete')
print('-------------------------')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

class Main_Commands():
    def __init__(self, bot):
        self.bot = bot

# Posts link to op.gg profile of 'ign'
@bot.command()
async def opgg(*, ign: str):
    pattern = re.compile(r'\s+')
    ign = re.sub(pattern, '+', ign)
    await bot.say('http://na.op.gg/summoner/userName={}'.format(ign))

# Posts a random image of 'name' from zerochan.net
@bot.command()
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
    await bot.say(imageUrl)

# Return MAL link for the anime 'title' using myanimelist.net's api
@bot.command()
async def mal(*, title: str):
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

    await bot.say(url)

# The bot will comment with a mp4 link of an OP from /r/AnimeThemes for a given anime
@bot.command()
async def op(*, titlez: str):
    openings = findAnimeOpening(titlez)
    # Most likely an invalid anime title
    if(openings == -1): 
        await bot.say('I couldn\'t find any openings for this anime you potato <:PunOko:370486584153473024>')
        return

    # Prevent the bot from spamming too many links because of bad requests
    if(len(openings) > 8):
        await bot.say('This request has too many links')
        return

    comment = ''

    comment += '<:VoHiYo:370487040380239872> Here are the opening(s) for \"' + titlez + '\" <:VoHiYo:370487040380239872>\n'
    for anime in openings:
        if('reddit' not in anime.url):
            comment += anime.title + '\n'
            comment += anime.url + '\n'

    comment += '<:TehePelo:370494286707425280> Not what you were looking for? Check the title of the anime and try again! <:TehePelo:370494286707425280>'
    await bot.say(comment)

# The bot will comment with a mp4 link of an ED from /r/AnimeThemes for a given anime
@bot.command()
async def ed(*, title: str):
    endings = findAnimeEnding(title)
    if(endings == -1):
        await bot.say('I couldn\'t find any endings for this anime you ape <:PunOko:370486584153473024>')
        return

    # Prevent the bot from spamming too many links because of bad requests
    if(len(endings) > 8):
        await bot.say('This request has too many links')
        return

    comment = ''
    comment += '<:VoHiYo:370487040380239872> Here are the ending(s) for \"' + title + '\" <:VoHiYo:370487040380239872>\n'
    for anime in endings:
        if('reddit' not in anime.url):
            comment += anime.title + '\n'
            comment += anime.url + '\n'

    comment += '<:TehePelo:370494286707425280> Not what you were looking for? Check the title of the anime and try again! <:TehePelo:370494286707425280>'
    await bot.say(comment)

# Retrieves a random post from /r/anime_irl
@bot.command()
async def me_irl():
    url = randomPost('anime_irl')
    await bot.say(url)

# Retrieves a random post from /r/awwnime
@bot.command()
async def cute():
    url = randomPost('awwnime')
    await bot.say(url)

@bot.command()
async def lewd():
    url = randomPost('ZettaiRyouiki+pantsu')
    await bot.say(url)


# taken from https://github.com/Nihilate/Roboragi/blob/master/roboragi/MAL.py
def convertXML(text):
    import html.parser

    text = text.replace('&Eacute;', 'É').replace('&times;', 'x').replace('&rsquo;', "'").replace('&lsquo;', "'").replace('&hellip', '...').replace('&le', '<').replace('<;', '; ').replace('&hearts;', '♥').replace('&mdash;', '-')
    text = text.replace('&eacute;', 'é').replace('&ndash;', '-').replace('&Aacute;', 'Á').replace('&acute;', 'à').replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&Oslash;', 'Ø').replace('&frac12;', '½').replace('&infin;', '∞')
    text = text.replace('&agrave;', 'à').replace('&egrave;', 'è').replace('&dagger;', '†').replace('&sup2;', '²').replace('&#039;', "'")

    return text

    text=html.parser.HTMLParser().unescape(text)
    return html.parser.HTMLParser().unescape(text)
  
bot.run(config.token)
