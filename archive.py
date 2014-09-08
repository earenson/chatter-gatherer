'''
@author Eric Arenson
@date Jul 9, 2014
@license CC BY-NC-SA 4.0: http://creativecommons.org/licenses/by-nc-sa/4.0/

This script uses the Twitter API to archive Twitter Chats by hashtag. 
Uses Python Twitter Tools (https://github.com/sixohsix/twitter)

Store your varibales in config.py (See sample.config.py for reference)
'''

from twitter import *
from config import *
import sqlite3
import time
import json

# Globals
max_id = 0

# This is used to stop get_tweets from recursing into infinity
page_count = 0

# Connect to sqlite DB
con = sqlite3.connect('database.db')
cur = con.cursor()

def get_chat_id():
	# Since this runs only on a Thursday, it's safe to say that we can 
	# create a new chat record when this runs.
	today = time.strftime('%d-%m-%Y')
	# cur.execute("INSERT INTO chats (created_at) VALUES(?)", (today,))
	# con.commit()

	# Get today's chat ID so we can link the tweets to it
	cur.execute("SELECT id FROM chats WHERE created_at=?", (today,))
	chat_id = cur.fetchone()[0]

def get_tweets(max_id):

	t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
	if(max_id == 0):
		# Get tweets
		chat = t.search.tweets(q="#uxchat", until="2014-07-05")
		#print chat
		
		max_id = chat['search_metadata']['max_id']
		tweets = chat['statuses']
	else: 
		chat = t.search.tweets(q="#uxchat", max_id=max_id)
		max_id = chat['search_metadata']['max_id']
		page_count += 1

	return tweets
	check_for_more(max_id)

def check_for_more(max_id):
	print max_id

def write_to_json(tweets):
	# Write to file for testing
	f = open('sample.json', 'w')
	f.write(json.dumps(tweets))
	f.close()

def write_to_db(tweets):

	for i in tweets:

		# CHECK: Does this tweet ID exist? If not, insert into tweets
		cur.execute("SELECT id FROM tweets WHERE id=?", (i['id'],))
		data = cur.fetchone()
		if data is None:
			cur.execute("INSERT INTO tweets VALUES(?,?,?,?,?,?,?,?,?)", (i['id'], i['created_at'], i['user']['id'], i['text'], i['favorite_count'], i['retweet_count'],i['in_reply_to_status_id'], i['in_reply_to_user_id'], chat_id)) 
			con.commit()

		# CHECK: Does this user exist? If not, insert into users
		cur.execute("SELECT user_id FROM users WHERE user_id=?", (i['user']['id'],))
		data = cur.fetchone()
		if data is None:
			cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?)",(i['user']['id'],i['user']['location'],i['user']['profile_image_url'],i['user']['name'],i['user']['screen_name'],i['user']['url']))
			con.commit()

def main():
	# Initial Call
	tweets = get_tweets(max_id)
	write_to_db(tweets)

if __name__ == "__main__":
	main()