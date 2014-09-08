'''
Website for Twitter Chat Archiver
'''

import web

render = web.template.render('html/')

# Setting up the URL handler
urls = (
	'/', 'index',
	'/user', 'user',
	'/chats/(.*)','chats'
)

# Connect to the database
db = web.database(dbn='sqlite', db='database.db')

# Defining the pages
class index: 
	def GET(self):
		# Get a list of all users
		users = db.query("SELECT name, profile_image_url FROM users")
		print users
		# Get a list of the archived chats to choose from
		chats = db.query("SELECT * FROM chats")

		return render.index(users, chats)

class user:
	def GET(self):
		return "Hey users!"

class chats:
	def GET(self, chat_id):

		#  Get tweets that are part of the chat requested
		

		tweets = db.query("SELECT * FROM tweets t join chats c on t.chat_id = c.id join users u on u.user_id = t.user_id WHERE t.chat_id=$id", vars={'id':int(chat_id)})
		
		# # Need to do a JOIN to get user data to display here
		# if tweets == False:
		# 	tweets = "No records"
		# for i in tweets:
		# 	print i
			
		return render.chats(tweets)

if __name__ == "__main__":
	app = web.application(urls,globals())
	app.run()