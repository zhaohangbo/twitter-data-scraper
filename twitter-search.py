#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
import os

#-----------------------------------------------------------------------
# twitter-search
#  - performs a basic keyword search for tweets containing the keywords
#    "lazy" and "dog"
#-----------------------------------------------------------------------

# Set a parser object
parser = argparse.ArgumentParser()
### Mandatory Parameters
parser.add_argument("--search_words", type=str, help="search_words: your target search key words")
args = parser.parse_args()
search_words = args.search_words

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
# perform a basic search
# Twitter API docs:
# https://dev.twitter.com/rest/reference/get/search/tweets
#-----------------------------------------------------------------------
# search_words ="good "
# count, the number of status
query = twitter.search.tweets(q = "' "+ search_words + " '", count = 500)

#-----------------------------------------------------------------------
# How long did this query take?
#-----------------------------------------------------------------------
print "Search complete (%.8f seconds)" % (query["search_metadata"]["completed_in"])

#-----------------------------------------------------------------------
# Loop through each of the results, and print its content.
#-----------------------------------------------------------------------

def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

def write_to_csv(file_name):
    global search_words

    if not os.path.exists('csv'):
        os.makedirs('csv')

    with open('csv/{}_data.csv'.format(file_name), 'w') as file:
        w = csv.writer(file)
        w.writerow(["search_words", "created_at" , "user_screen_name", "text"])
        for result in query["statuses"]:
            # print "(%s) @%s %s" % (result["created_at"], result["user"]["screen_name"], result["text"])
            created_at = '' if 'created_at' not in result else unicode_decode(str(result['created_at']))
            user_screen_name = '' if 'screen_name' not in  result["user"] else unicode_decode(result["user"]["screen_name"])
            text = '' if 'text' not in result  else unicode_decode(result['text'])
            w.writerow([search_words, created_at , user_screen_name, text ])

if __name__ == '__main__':
    print "search_words = " +  search_words
    write_to_csv(search_words+"_twitter_search")
