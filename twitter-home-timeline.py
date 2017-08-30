#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
import os

#-----------------------------------------------------------------------
# twitter-hoome-timeline:
#  - uses the Twitter API and OAuth to log in as your username,
#    and lists the latest 50 tweets from people you are following
#-----------------------------------------------------------------------

# Set a parser object
parser = argparse.ArgumentParser()
### Mandatory Parameters
parser.add_argument("--twitter_name", type=str, help="twitter_name: your target twitter account name ")
args = parser.parse_args()
username  = args.twitter_name

from twitter import *

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

#-----------------------------------------------------------------------
# request my home timeline
# twitter API docs: https://dev.twitter.com/rest/reference/get/statuses/home_timeline
#-----------------------------------------------------------------------

statuses_limit = 50
statuses = twitter.statuses.home_timeline(count = statuses_limit) # latest 50 statuses
print statuses

#-----------------------------------------------------------------------
# loop through each of my statuses, and print its content
#-----------------------------------------------------------------------

def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

def write_to_csv(file_name):
    if not os.path.exists('csv'):
        os.makedirs('csv')

    with open('csv/{}_data.csv'.format(file_name), 'w') as file:
        w = csv.writer(file)
        w.writerow(["created_at" ,"user_screen_name", "text"])
        for status in statuses:
            print "(%s) @%s %s" % (status["created_at"], status["user"]["screen_name"], status["text"])
            created_at = '' if 'created_at' not in status else unicode_decode(str(status['created_at']))
            user_screen_name = '' if 'screen_name' not in status["user"] else unicode_decode(status["user"]["screen_name"])
            text = '' if 'text' not in status else unicode_decode(status['text'])
            w.writerow([ created_at ,user_screen_name  , text])

if __name__ == '__main__':
    write_to_csv("my_twitter_home_timeline")
