#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
#import subprocess
import os

#-----------------------------------------------------------------------
# twitter-retweets
#  - print who has retweeted tweets from a given user's timeline
#-----------------------------------------------------------------------

# Set a parser object
parser = argparse.ArgumentParser()
### Mandatory Parameters
parser.add_argument("--twitter_name", type=str, help="twitter_name: your target twitter account name ")
args = parser.parse_args()
username  = args.twitter_name

from twitter import *

user = "ideoforms"

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
# perform a basic search
# twitter API docs: https://dev.twitter.com/rest/reference/get/statuses/user_timeline
#-----------------------------------------------------------------------

# Needed to write tricky unicode correctly to csv
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

#-----------------------------------------------------------------------
# loop through each of my statuses, and print its content
#-----------------------------------------------------------------------


def write_to_csv(file_name):
    if not os.path.exists('csv'):
        os.makedirs('csv')

    global user
    results = twitter.statuses.user_timeline(screen_name = user)
    with open('csv/{}_data.csv'.format(file_name), 'w') as file:
        w = csv.writer(file)
        w.writerow(["user", "text", "retweets", "retweets_count"])
        for status in results:
            user = unicode_decode(user)
            text = '' if 'text' not in status else unicode_decode(status["text"])
            #-----------------------------------------------------------------------
            # do a new query: who has retweet this tweet?
            #-----------------------------------------------------------------------
            retweets = twitter.statuses.retweets._id(_id = status["id"])
            retweeted_records = []
            for retweet in retweets:
                s = " - retweeted by %s" % (retweet["user"]["screen_name"])
                retweeted_records.append(s)
            retweets_count = len(retweeted_records)
            print retweeted_records
            retweeted_records_str = "\n".join(retweeted_records)
            print "~~~~"
            print retweeted_records_str
            w.writerow([user, text, retweeted_records_str , retweets_count])

if __name__ == '__main__':
    print "twitter_name = " +  username
    write_to_csv(username+"_twitter_list_retweets")
