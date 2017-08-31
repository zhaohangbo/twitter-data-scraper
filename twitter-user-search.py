#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
import os

#-----------------------------------------------------------------------
# twitter-user-search
#  - performs a search for users matching a certain query
#-----------------------------------------------------------------------

# Set a parser object
parser = argparse.ArgumentParser()
### Mandatory Parameters
parser.add_argument("--search_words", type=str, help="search_words : your target search_words ")
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
# perform a user search
# twitter API docs: https://dev.twitter.com/rest/reference/get/users/search
#-----------------------------------------------------------------------
# search_words = '"New Cross"'
results = twitter.search.tweets(q = "' "+ search_words + " '" , count = 500)

#-----------------------------------------------------------------------
# loop through each of the users, and print their details
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
        w.writerow(["search_words", "name", "user_screen_name" , "user_location"])
        for user in results:
            # print "@%s (%s): %s" % (user["screen_name"], user["name"], user["location"])
            name = '' if 'verified' not in user else unicode_decode(user['name'])
            screen_name= '' if 'screen_name' not in user else unicode_decode(user['screen_name'])
            location= '' if 'location' not in user else unicode_decode(user['location'])
            w.writerow([search_words, name, screen_name, location])

if __name__ == '__main__':
    print "search_words= " +  search_words
    write_to_csv(search_words+"_twitter_user_search")

