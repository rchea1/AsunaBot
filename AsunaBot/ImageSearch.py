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
		''' Retrieves a random image from https://anime-pictures.net '''
		imageArray = []
		name = name.replace(' ', '_')

		url = 'https://anime-pictures.net/pictures/view_posts/0?type=json&search_tag={}&lang=en'.format(name)
		anime = requests.get(url).json()

		if anime['posts_count'] == 0:
			await self.bot.send_message(ctx.message.channel, 'No results for "{}"'.format(name))
			return

		pageNumbers = int(anime['max_pages'])

		randomPage = 0

		if(pageNumbers > 0):
			randomPage = random.randint(0, pageNumbers)
		
		print('Getting random image of "{}" from page {}'.format(name, randomPage))
		url = 'https://anime-pictures.net/pictures/view_posts/{}?type=json&search_tag={}&lang=en'.format(randomPage, name)    
		data = requests.get(url).json()

		random_image = random.randint(0, int(data['response_posts_count'])-1)

		image_id = str(data['posts'][random_image]['id'])
		extension = str(data['posts'][random_image]['ext'])
		image_link = str(data['posts'][random_image]['big_preview'])
		image_link = image_link.replace('.webp', '')

		# Downloading the image for myself and uploading the file through discord
		filepath = os.path.join(config.IMAGE_PATH, image_id + extension)
		urllib.request.urlretrieve(image_link, filepath)
		await self.bot.send_file(ctx.message.channel, config.IMAGE_PATH + image_id + extension)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('~'), description='Image search')
bot.add_cog(ImageSearch(bot))

def setup(bot):
	bot.add_cog(ImageSearch(bot))
