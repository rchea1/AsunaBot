import discord
import config
import asyncio
import os
import requests
import urllib
import random

import xml.etree.cElementTree as ET
from discord.ext import commands

client = discord.Client()

class ImageSearch:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context = True, no_pm = True)
	async def showme(self, ctx, *, name: str):
		''' Retrieves a random image from https://konachan.com '''
		imageArray = []
		name = name.replace(' ', '_')
		url = 'https://konachan.com/post.json?tags={}&limit=100'.format(name)    
		data = requests.get(url).json()
		
		konachan = requests.Session()
		request = konachan.get('https://konachan.com/post.xml?tags={}'.format(name))
		konachan.close()
		request = ET.fromstring(request)
	
		print(request)

		for image in data:
			info = {'image_link': 'https:' + str(image['jpeg_url']),
					'id': image['id']}
			imageArray.append(info)

		print('Getting random image of:  ' + name)
		image = random.choice(imageArray)
		filepath = os.path.join(config.IMAGE_PATH, str(image['id']) + '.jpg')
		urllib.request.urlretrieve(image['image_link'], filepath)
		await self.bot.send_file(ctx.message.channel, config.IMAGE_PATH + str(image['id']) + '.jpg')

bot = commands.Bot(command_prefix=commands.when_mentioned_or('~'), description='Image search')
bot.add_cog(ImageSearch(bot))

def setup(bot):
	bot.add_cog(ImageSearch(bot))