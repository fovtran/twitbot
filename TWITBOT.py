import oauth2 as oauth
import json
import urllib
import re
from numpy import array, sort
from JsonConfiguration import *


authorize_token_url= "https://api.twitter.com/oauth/authorize"
request_token_url= "https://api.twitter.com/oauth/request_token"
access_token_url= "https://api.twitter.com/oauth/access_token"

twitter_api_statuses = "https://api.twitter.com/1.1/statuses"
twitter_api_timeline = "https://api.twitter.com/1.1/statuses/user_timeline.json"
twitter_api_update = "https://api.twitter.com/1.1/statuses/update.json"
twitter_api_home = "https://api.twitter.com/1.1/statuses/home_timeline.json"
twitter_api_search = "https://api.twitter.com/1.1/search/tweets.json"

#data = urllib.parse.urlencode( {'user_id': 'lopitalch'} )

def consumer():
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, token)
	resp, content = client.request(access_token_url, "POST")
	return client


def get_home(client):
	resp, data = client.request(twitter_api_home, method="GET")
	tweets = json.loads(data)
	for tweet in tweets:
		print(tweet['text'])
		print('--------------------------------')

def get_query(client):
	query = "big%20data&count=100&result_type=recent" #popular!recent
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
	print(data)
	return resp

def post_tweet(client, msg):
	# { 'display_coordinates': 'true', 'lat': '', 'long': '', 'media_ids': ''}
	data = urllib.parse.urlencode( {'status': msg} )
	resp, data = client.request(twitter_api_update, body=(data, "utf-8"), method="POST")

username = 'your-twitter-username'
client = consumer()

# Launch a refined twitter search. Parse some stats
# get_query(client)

# Get your timeline tweets (your follows tweets)
# get_home(client)

# Post a Tweet
# post_tweet(client, 'save me lord,')

# Show your current tweets up to N. In reverse order
N = 3
ids, tweets = get_timeline(client, username, 3)
tweets.reverse()
for twit in tweets:
	print(twit)

# Ask to delete latest N tweets
query = input('Delete current Tweets? [Y/N]: ')
if query=='Y':
	about_id_rm=True
	for i in ids:
		if about_id_rm:
			print('Id:%i'%i)
			ret = destroy_timeline(client,i)
