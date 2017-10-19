# Utilizes Reddit's API to search for openings and eventually endings for 
# a specified anime from /r/AnimeThemes

import praw 
import config
import re
import random

def startup():
	print('Authenticating Reddit...')
	reddit = praw.Reddit(config.USER, user_agent = config.user_agent)
	return reddit

# Finds the opening from /r/AnimeThemes
# @title is the title of the anime 
def findAnimeOpening(title):
	print('Searching for OPs for ' + title)
	reddit = startup()
	openings = []

	for submission in reddit.subreddit('animethemes').search(title, 'new'):
		if submission.link_flair_text == 'Added to wiki' and 'OP' in submission.title:
			openings.append(submission)

	if not openings:
		print('Could not find any openings for this anime')
		return -1

	return list(reversed(openings))

# Finds the endings from /r/AnimeThemes
# @title is the title of the anime 
def findAnimeEnding(title):
	print('Searching for EDs for ' + title)
	reddit = startup()
	endings = []

	for submission in reddit.subreddit('animethemes').search(title, 'new'):
		if submission.link_flair_text == 'Added to wiki' and 'ED' in submission.title:
			endings.append(submission)

	if not endings:
		print('Could not find any openings for this anime')
		return -1

	return list(reversed(endings))

def randomIrlPost():
	print('Getting random /r/anime_irl post')
	reddit = startup()
	array = []

	for submission in reddit.subreddit('anime_irl').hot(limit = 100):
		array.append(submission.url)

	return(random.choice(array))
