#!/usr/bin/python
import sys
import subprocess
import argparse # Using argparse to parse cli arguments
import datetime

# input date formatted as YYYY-MM-DD
date_now = datetime.datetime.now().strftime ("%Y-%m-%d")
time_delta = 7
date_7_days_ago = (datetime.datetime.now() - datetime.timedelta(days= time_delta)).strftime ("%Y-%m-%d")
since_date_default = date_7_days_ago  #"2017-07-8"
until_date_default = date_now #"2017-07-15"

# Set a parser object
parser = argparse.ArgumentParser()
### Mandatory Parameters
parser.add_argument("--search_words", type=str, help="--search_words: target twitter account name")
### Optional Parameters
#parser.add_argument("--since_date",type=str, default= since_date_default,
#                    help="since_date to scrape (format YYYY-MM-DD , default today-7days)")
#parser.add_argument("--until_date",type=str, default= until_date_default,
#                    help="util_date to scrape (format YYYY-MM-DD , default today)")

args = parser.parse_args()
search_words= args.search_words
#since_date   = args.since_date
#until_date   = args.until_date

runnable_files = [
        "twitter-search-geo.py",
        "twitter-search.py",
        "twitter-user-search.py",
]

def do_search():
    for run_file in runnable_files:
        print "running : " + run_file
        cmd = "python " + run_file + "  --search_words " + search_words
        print "cmd is : " + cmd
        subprocess.call(cmd, shell=True)
        #time.sleep(60)
    sys.exit(-1)

def main():
    print "searching your target key words"
    do_search()

if __name__ == "__main__":
    main()
