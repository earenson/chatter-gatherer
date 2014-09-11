chatter-gatherer
================

A small Python-based script to collect and display Twitter chats according to hashtag.

## Setup
This script uses SQLite to store tweets, so the first thing you'll need to do is run `python db_init.py`. This will create the empty database necessary.

## Collecting Tweets
To collect tweets, run `python stream.py` and pass the hashtag you want to collect to it as an argument. For example: `python stream.py github` will collect tweets with #github.

## Displaying Tweets
The script requires web.py (http://webpy.org/) to display the tweets from database as a website. To start the framework, run `python display.py`. By default, this will create a website accessible by visiting localhost:8080.

## TODOs
1. Style the html display pages
2. Separate questions, answers, and topics by format (Q1, A1, TOPIC) in tweet content