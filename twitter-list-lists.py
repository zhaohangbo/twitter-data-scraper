#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
import os

# Set a parser object
parser = argparse.ArgumentParser()
### Mandatory Parameters
parser.add_argument("--twitter_name", type=str, help="twitter_name: your target twitter account name ")
args = parser.parse_args()
user  = args.twitter_name

#-----------------------------------------------------------------------
# twitter-list-lists
#  - lists the lists owned by each of a list of users
#-----------------------------------------------------------------------

from twitter import *


#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

import pprint

def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

#-----------------------------------------------------------------------
# the list of users that we want to examine
#-----------------------------------------------------------------------
#users = [ "ideoforms", "hrtbps", "mocost", "SportPesa", "realmadrid"]

#-----------------------------------------------------------------------
# for each of our users in turn...
#-----------------------------------------------------------------------
def write_to_csv(file_name):
    if not os.path.exists('csv'):
        os.makedirs('csv')

    with open('csv/{}_data.csv'.format(file_name), 'w') as file:
        w = csv.writer(file)
        w.writerow(["user", "list_name" , "list_member_count"])
        #print "@%s" % (user)
        #-----------------------------------------------------------------------
        # ...retrieve all of the lists they own.
        # twitter API docs: https://dev.twitter.com/rest/reference/get/lists/list
        #-----------------------------------------------------------------------
        result = twitter.lists.list(screen_name = user)
        for list in result:
            print " - %s (%d members)" % (list["name"], list["member_count"])
            list_name = '' if 'name' not in list else unicode_decode(str(list['name']))
            list_member_count = '' if 'member_count' not in list else unicode_decode(str(list['member_count']))
            w.writerow([user, list_name , list_member_count])

if __name__ == '__main__':
    print "twitter_name = " +  user
    write_to_csv(user+"_twitter_list_lists")
