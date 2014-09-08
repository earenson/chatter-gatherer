'''
stream.py
Description: Used to collect twitter chats via the Stream API
'''

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import time
import sqlite3
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

# TWITTER API CREDENTIALS (move to config.ini)
access_token = parser.get('twitter','access_token')
access_secret = parser.get('twitter','access_secret')
consumer_key = parser.get('twitter','consumer_key')
consumer_secret = parser.get('twitter','consumer_secret')

# SET UP TWITTER OAUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# CONNECT TO DB
con = sqlite3.connect('database.db')
cur = con.cursor()

# LISTENER CLASS
class listener(StreamListener):

	def on_status(self, status):
		write_to_db(status)
		print "Tweet ID %s from %s written." % (status.id, status.user.name)
		return True

	def on_error(self, status):
		print status

# FUNCTIONS
def get_chat_id():
	# Since this runs only on a Thursday, it's safe to say that we can 
	# create a new chat record when this runs.
	today = time.strftime('%d-%m-%Y')
	# cur.execute("INSERT INTO chats (created_at) VALUES(?)", (today,))
	# con.commit()

	try:
		# Get today's chat ID so we can link the tweets to it
		cur.execute("SELECT id FROM chats WHERE created_at=?", (today,))
		return cur.fetchone()[0]
	except:
		cur.execute("INSERT INTO chats (created_at) VALUES(?)", (today,))
		print "New chat created: %s" % today


def write_to_db(tweet):

	chat_id = get_chat_id()

	# CHECK: Does this tweet ID exist? If not, insert into tweets
	cur.execute("SELECT id FROM tweets WHERE id=?", (tweet.id,))
	data = cur.fetchone()
	if data is None:
		cur.execute("INSERT INTO tweets VALUES(?,?,?,?,?,?,?,?,?)", (tweet.id, tweet.created_at, tweet.user.id, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_status_id, tweet.in_reply_to_user_id, chat_id)) 
		con.commit()

	# CHECK: Does this user exist? If not, insert into users
	cur.execute("SELECT user_id FROM users WHERE user_id=?", (tweet.user.id,))
	data = cur.fetchone()
	if data is None:
		cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?)",(tweet.user.id,tweet.user.location, tweet.user.profile_image_url,tweet.user.name, tweet.user.screen_name, tweet.user.url))
		con.commit()

# GO!
if __name__ == "__main__":
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=["yolo"])