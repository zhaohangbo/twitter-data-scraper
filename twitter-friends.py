#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
#import subprocess
import os

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
#find all the following of the target user

#-----------------------------------------------------------------------
# twitter-friends
#  - lists all of a given user's friends (ie, followees)
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
# this is the user whose friends we will list
#-----------------------------------------------------------------------
#username = "ideoforms"

#-----------------------------------------------------------------------
# perform a basic search
# twitter API docs: https://dev.twitter.com/rest/reference/get/friends/ids
#-----------------------------------------------------------------------
query = twitter.friends.ids(screen_name = username)

#-----------------------------------------------------------------------
# tell the user how many friends we've found.
# note that the twitter API will NOT immediately give us any more
# information about friends except their numeric IDs...
#-----------------------------------------------------------------------
print "found %d friends" % (len(query["ids"]))


# Needed to write tricky unicode correctly to csv
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

#-----------------------------------------------------------------------
# now we loop through them to pull out more info, in blocks of 100.
#-----------------------------------------------------------------------

def write_to_csv(file_name):
    if not os.path.exists('csv'):
        os.makedirs('csv')

    with open('csv/{}_data.csv'.format(file_name), 'w') as file:
        w = csv.writer(file)
        w.writerow(["user_verified", "user_screen_name" , "user_location"])
        for n in range(0, len(query["ids"]), 100):
            ids = query["ids"][n:n+100]

            #-----------------------------------------------------------------------
            # create a subquery, looking up information about these users
            # twitter API docs: https://dev.twitter.com/rest/reference/get/users/lookup
            #-----------------------------------------------------------------------
            subquery = twitter.users.lookup(user_id = ids)

            for user in subquery:
                #-----------------------------------------------------------------------
                # now print out user info, starring any users that are Verified.
                #-----------------------------------------------------------------------
                # print " [%s] %s - %s" % ("*" if user["verified"] else " ", user["screen_name"], user["location"])

                #status_message = '' if 'message' not in status else unicode_decode(status['message'])
                #link_name = '' if 'name' not in status else unicode_decode(status['name'])
                #status_link = '' if 'link' not in status else unicode_decode(status['link'])
                verified= '' if 'verified' not in user else unicode_decode(str(user['verified']))
                screen_name= '' if 'screen_name' not in user else unicode_decode(user['screen_name'])
                location= '' if 'location' not in user else unicode_decode(user['location'])

                w.writerow([verified, screen_name, location])
                #w.writerow([str(user["verified"]), user["screen_name"], user["location"]])
                #w.writerow(["status_id", "status_message", "link_name", "status_type", "status_link", "status_published", "num_reactions", "num_comments", "num_shares", "num_likes", "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys","num_special"])
                #w.writerow(status_data + reactions_data + (num_special,))


if __name__ == '__main__':
    print "twitter_name = " +  username
    write_to_csv(username+"_twitter_friends")
