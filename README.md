chatter-gatherer
================

A small Python-based script to collect and display Twitter chats according to hashtag.

## Setup
You'll first need to create a file called `config.ini` containing your Twitter API credentials. Use `sample.config.ini` as a reference.

This script uses SQLite to store tweets, so the first thing you'll need to do is run `python db_init.py`. This will create the empty database necessary.

## Collecting Tweets
To collect tweets, run `python stream.py` and pass the hashtag you want to collect to it as an argument. For example: `python stream.py github` will collect tweets with #github.

## Displaying Tweets
The script requires web.py (http://webpy.org/) to display the tweets from database as a website. To start the framework, run `python display.py`. By default, this will create a website accessible by visiting localhost:8080.

## TODOs
1. Style the html display pages
2. Revisit how chats are marked - currently it uses the date, but that won't work for collecting multiple chats on the same day