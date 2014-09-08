'''
Used to initialize the sqlite database.
Only needs to be run once (or just distribute the package with a blank db)
'''

import sqlite3

con = sqlite3.connect('database.db')

con.execute('''CREATE TABLE tweets (
		id bigint,
		created_at date,
		user_id bigint,
		text text,
		favorite_count int,
		retweet_count int,
		in_reply_to_status_id bigint,
		in_reply_to_user_id bigint
		chat_id int,
		PRIMARY KEY (id)
	)
''')
con.execute('''CREATE TABLE users (
		user_id bigint,
		location text,
		profile_image_url text,
		name text,
		screen_name text,
		url text,
		PRIMARY KEY (user_id)
	)
''')
con.execute('''CREATE TABLE chats (
		id INTEGER,
		created_at date,
		PRIMARY KEY (id)
	)
''')

con.commit()
con.close()
