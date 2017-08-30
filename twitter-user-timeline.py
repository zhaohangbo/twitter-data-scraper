#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
import os

#-----------------------------------------------------------------------
# twitter-user-timeline
#  - displays a user's current timeline.
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
# this is the user we're going to query.
#-----------------------------------------------------------------------
user = username

#-----------------------------------------------------------------------
# query the user timeline.
# twitter API docs:
# https://dev.twitter.com/rest/reference/get/statuses/user_timeline
#-----------------------------------------------------------------------
results = twitter.statuses.user_timeline(screen_name = user)

#-----------------------------------------------------------------------
# loop through each status item, and print its content.
#-----------------------------------------------------------------------


def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

def write_to_csv(file_name):
    global user
    if not os.path.exists('csv'):
        os.makedirs('csv')

    with open('csv/{}_data.csv'.format(file_name), 'w') as file:
        w = csv.writer(file)
        w.writerow(["user", "created_at" , "text"])
        for status in results:
            # print "(%s) %s" % (status["created_at"], status["text"].encode("ascii", "ignore"))
            created_at = '' if 'created_at' not in status else unicode_decode(str(status['created_at']))
            text = '' if 'text' not in status else unicode_decode(status['text'])
            w.writerow([user, created_at , text])

if __name__ == '__main__':
    print "twitter_name = " +  username
    write_to_csv(username+"_twitter_user_timeline")
