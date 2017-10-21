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
	print('Searching OPs for ' + title)
	reddit = startup()
	openings = []

	for submission in reddit.subreddit('animethemes').search(title, 'new'):
		if submission.link_flair_text == 'Added to wiki' and 'OP' in submission.title:
			openings.append(submission)
		else: 
			if submission.link_flair_text == 'Mirror in Comments' and 'OP' in submission.title:
				for comment in submission.comments.list():
					if('https' in comment.body):
						url = comment.body.split('Mirror: ')[1]
						submission.url = url
						openings.append(submission)
						break

	if not openings:
		print('Could not find any openings for this anime')
		return -1

	return list(reversed(openings))

# Finds the endings from /r/AnimeThemes
# @title is the title of the anime 
def findAnimeEnding(title):
	print('Searching EDs for ' + title)
	reddit = startup()
	endings = []

	for submission in reddit.subreddit('animethemes').search(title, 'new'):
		if submission.link_flair_text == 'Added to wiki' and 'ED' in submission.title:
			endings.append(submission)
		else: 
			if submission.link_flair_text == 'Mirror in Comments' and 'ED' in submission.title:
				for comment in submission.comments.list():
					if('https' in comment.body):
						url = comment.body.split('Mirror: ')[1]
						print(url)
						submission.url = url
						endings.append(submission)
						break

	if not endings:
		print('Could not find any endings for this anime')
		return -1

	return list(reversed(endings))

def randomPost(subreddit):
	print('Getting random post from /r/' + subreddit)
	reddit = startup()
	array = []

	for submission in reddit.subreddit(subreddit).top('all'):
		array.append(submission.url)

	return(random.choice(array))

	return sub
