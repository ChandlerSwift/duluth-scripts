#!/usr/bin/python3

import re
import tweepy
import picamera
import os
import requests
from colour import Color
import datetime
from getpass import getpass
from time import sleep
debug_enabled=False

def debug(message):
    if debug_enabled:
        print("DEBUG (" + str(datetime.datetime.now()) + "):")

def post_success(post):
    print("     Replied: https://twitter.com/swftbot/status/"+str(post.id))

class MyStreamListener(tweepy.StreamListener):

    num_processed = 0

    debug = False
    
    def on_status(self, status):
        # Verify that tweet is by @jakewazz
        if status.user.screen_name != "JakeWazz":
            debug("Ignored tweet")
            return


        # Log information
        self.num_processed += 1
        print(str(self.num_processed).zfill(3) + ". " +
              "New incoming tweet from " + status.user.screen_name + ": " +
              status.text)
        post_success(twitter.update_status("@" + status.user.screen_name + " Gosh Darn!",
                                           in_reply_to_status_id=int(status.id_str)))

        debug("handling complete")


# TWITTER SETUP
CONSUMER_KEY = 'LIgyONB0Yo5iPVSNmfacviZ7Q'
CONSUMER_SECRET = 'vWxsquWsQ6tNFykdIelIVmdYpvwHK9Nf7DeJxtSHSPxz8z20sx'
ACCESS_KEY = '750044898431078400-45uLPrttY4Pct2kjdiCS3eGCZjVV9NU'
ACCESS_SECRET = 'kY1uPa55HoH5EStyK0tuSgZJE41KjQBgsH4O1Ai9zF7lr'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter = tweepy.API(auth)

# STREAM TWEETS
print("Streaming from Twitter...")
while True:
    try:
        myStream = tweepy.Stream(auth=twitter.auth, listener=MyStreamListener())
        myStream.filter(track=['JakeWazz'], async=True)
    except Exception as e:
        print('ERROR STREAMING: %s' % e)
