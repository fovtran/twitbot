# -*- coding: utf-8 -*-

"""\
Simple Twitter Automation Bot. (Python ~3.7)
=============================================================

Requires Oauth2 -> "pip install oauth2"
"""
__title__ = 'Twitbot'
__author__ = "DMC Creations."
__credits__ = ["Diego C."]
__email__ = "dcadogan@live.com.ar"
__version__ = "0.5.2"
__status__ = "RC1"
__maintainer__ = "Beta"
__license__ = "LGPL"
__copyright__ = "Copyright 2018, "

import oauth2 as oauth
import json
import urllib
import re
from numpy import array, sort
from JsonConfiguration import *


authorize_token_url= "https://api.twitter.com/oauth/authorize"
request_token_url= "https://api.twitter.com/oauth/request_token"
access_token_url= "https://api.twitter.com/oauth/access_token"

def consumer():
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, token)
	resp, content = client.request(access_token_url, "POST")
	return client

twitter_api_statuses = "https://api.twitter.com/1.1/statuses"
twitter_api_timeline = "https://api.twitter.com/1.1/statuses/user_timeline.json"
twitter_api_update = "https://api.twitter.com/1.1/statuses/update.json"
twitter_api_home = "https://api.twitter.com/1.1/statuses/home_timeline.json"
twitter_api_search = "https://api.twitter.com/1.1/search/tweets.json"

def get_home(client):
	resp, data = client.request(twitter_api_home, method="GET")
	tweets = json.loads(data)
	for tweet in tweets:
		print(tweet['text'])
		print('--------------------------------')

def get_query(client):
	query = "Big%20Insight&count=100&result_type=recent" #popular!recent
	resp, data = client.request(twitter_api_search + "?q="+query, method="GET")
	tweets = json.loads(data.decode('utf-8'))
	hashlist = []
	hashhits = []
	for tweet in tweets['statuses']:
		tw = tweet['text']
		c = re.compile(r'\B#(\d*[a-zA-Z]+\w*)\b(?!;)')
		match = c.findall(tw)
		for hashtag in match:
			if hashtag not in hashlist:
				hashlist+=((hashtag),)
			else:
				hashhits+=((hashtag),)

	count = {}
	for h in hashhits:
		if h not in hashhits:
			count[h] = 1
		else:
			if h not in count.keys():
				count[h] = 0
				count[h] +=1
			else:
				count[h] = count[h]+1

	hashlist.sort()
	print(hashlist)
	print('--------------------------------')
	print(count)

def get_timeline(client,username, count):
	resp, data = client.request(twitter_api_timeline+"?user_id="+username+"&count="+str(count), method="GET")
	tweets = json.loads(data)
	tweet_data = []
	tweet_id = []
	for tweet in tweets:
		tweet_data.append(tweet['text'])
		tweet_id.append(tweet['id'])
	return tweet_id, tweet_data

def destroy_timeline(client,ID):
	resp, data = client.request(twitter_api_statuses+"/destroy/"+str(ID)+".json", method="POST")
	return resp, data

def post_tweet(client, msg):
	# { 'display_coordinates': 'true', 'lat': '', 'long': '', 'media_ids': ''}
	data = urllib.parse.urlencode( {'status': msg} )
	resp, data = client.request(twitter_api_update, body=(data, "utf-8"), method="POST")

username = 'nobody'
client = consumer()

# Launch a refined twitter search. Parse some stats
# get_query(client)

# Get your timeline tweets (your follows tweets)
# get_home(client)

# Post a Tweet
# post_tweet(client, 'save me lord,')

# Show your current tweets up to N. In reverse order

if len(sys.argv)>1:
	twitcount=int(sys.argv[1])
else:
	twitcount=1
ids, tweets = get_timeline(client, username, twitcount)
tweets.reverse()
for twit in tweets:
	print(twit)

query = input('Delete current Tweets? [Y/N]: ')
if query=='Y':
	about_id_rm=True
	for i in ids:
		if about_id_rm:
			print('Id:%i'%i)
			resp, data = destroy_timeline(client,i)
