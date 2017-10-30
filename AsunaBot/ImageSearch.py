import discord
import config
import asyncio
import os
import requests
import urllib
import random

import xml.etree.cElementTree as ET
from discord.ext import commands
from math import ceil

client = discord.Client()

class ImageSearch:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context = True, no_pm = True)
	async def showme(self, ctx, *, name: str):
		''' Retrieves a random image from https://konachan.com '''
		imageArray = []
		name = name.replace(' ', '_')
		
		konachan = requests.Session()
		request = konachan.get('https://konachan.com/post.xml?tags={}'.format(name))
		konachan.close()
		request = ET.fromstring(request.content)

		# konachan lists 21 images per page
		pageNumbers = int(request.attrib['count'])
		if pageNumbers == 0:
			await self.bot.send_message(ctx.message.channel, 'No images were found for the tag "{}"'.format(name))
			return
		if pageNumbers < 21: 
			pageNumbers = 1
		else:
			pageNumbers = int(ceil(pageNumbers / 21))

		# Getting a random page number if there are more than 1 page of images
		if pageNumbers > 0:
			randomPage = random.randint(0, pageNumbers)
			if randomPage == 0: 
				randomPage = 1
		else:
			randomPage = pageNumbers

		print('Getting random image of "{}" from page {}'.format(name, randomPage))
		url = 'https://konachan.com/post.json?page={}&tags={}&limit=21'.format(randomPage, name)    
		data = requests.get(url).json()
	
		for image in data:
			info = {'image_link': 'https:' + str(image['jpeg_url']),
					'id': image['id']}
			imageArray.append(info)

		image = random.choice(imageArray)
		# Downloading the image for myself and uploading the file through discord
		filepath = os.path.join(config.IMAGE_PATH, str(image['id']) + '.jpg')
		urllib.request.urlretrieve(image['image_link'], filepath)
		await self.bot.send_file(ctx.message.channel, config.IMAGE_PATH + str(image['id']) + '.jpg')

bot = commands.Bot(command_prefix=commands.when_mentioned_or('~'), description='Image search')
bot.add_cog(ImageSearch(bot))

def setup(bot):
	bot.add_cog(ImageSearch(bot))
