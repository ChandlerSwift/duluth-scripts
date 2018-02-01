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

password=getpass("Password for duluth.chandlerswift.com/light: ")

def debug(message):
    if debug_enabled:
        print("DEBUG (" + str(datetime.datetime.now()) + "):")

def post_success(post):
    print("     Replied: https://twitter.com/swftbot/status/"+str(post.id))

def post_bench_pic(status, text=""):
    camera.capture('tmp.jpg')
    debug(str(status.id))
    post_success(twitter.update_with_media(filename='tmp.jpg',
                                           status="@"+status.user.screen_name + " " + text,
                                           in_reply_to_status_id=int(status.id_str)))
    os.remove('tmp.jpg')

def set_light(command, query_append_string=""):
    #print("Nighttime autoresponse: https://twitter.com/swftbot/status/" +
    #      str(twitter.update_status("Sorry, light control is disabled at the moment.",
    #                                in_reply_to_status_id = status.id).id))

    if command == "on":
        rgb = [255,255,255]
    elif command == "off":
        rgb = [0,0,0]
    else:
        rgb = [int(a*255) for a in Color(command).rgb]

    base_url = "https://duluth.chandlerswift.com/light"
    url = base_url + "/light/set?1=%i&2=%i&3=%i&%s" % (rgb[0], rgb[1], rgb[2], query_append_string)
    requests.get(url, auth=('chandler@chandlerswift.com', password))

class MyStreamListener(tweepy.StreamListener):

    num_processed = 0

    debug = False
    
    def on_status(self, status):
        # Verify that tweet is @me, not by me
        if status.user.screen_name == "swftbot":
            debug("Ignored my own tweet")
            return

        if not status.text.startswith("@swftbot "):
            debug("Tweet from @" + status.user.screen_name + " ignored: " +
                  status.text)
            return

        # Log information
        self.num_processed += 1
        print(str(self.num_processed).zfill(3) + ". " +
              "New incoming tweet from " + status.user.screen_name + ": " +
              status.text)

        parsed = re.search("^@swftbot ([A-Za-z]*) ?(#?[A-Za-z]*)?.*$", status.text)
        if parsed is None:
            print("     No command found.")
            return

        command = parsed.group(1).lower()

        if command == "light":
            set_light(parsed.group(2), "twitter=%s" % status.user.screen_name)
            sleep(0.2)
            post_bench_pic(status)
        elif command == "bench":
            post_bench_pic(status)
        else:
            debug("Command not found")

        debug("handling complete")

# CAMERA SETUP
camera = picamera.PiCamera()

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
        myStream.filter(track=['swftbot'], async=True)
    except Exception as e:
        print('ERROR STREAMING: %s' % e)
