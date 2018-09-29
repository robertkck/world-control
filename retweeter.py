# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 19:05:49 2018

@author: rober
"""

import tweepy
from key import *
import pickle
from time import sleep

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

worldcontrol = api.search(q = "@truWorldControl", tweet_mode='extended')
since_id = worldcontrol[1].id
                       
import time
while True:
    print("loop")
    try:
        new_tweets = api.search(q = "@truWorldControl", since_id = since_id, tweet_mode='extended')
        if not new_tweets:
            print("No new tweet")
        else:
            for tweet in tweepy.Cursor(api.search, q='@truWorldControl', since_id = since_id, tweet_mode='extended').items(5):
                print("new tweet found: " + tweet.full_text)
                try:
                    if "#fakenewz" not in tweet.full_text:
                        print("Tweet does not include the #fakenewz Hashtag")
                    else:
                        print('\nBot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to respond.')
                        tweet.retweet()
                        print('Retweet published successfully.')
                except tweepy.TweepError as error:
                    print('\nError. Retweet not successful. Reason: ')
                    print(error.reason)
                except StopIteration:
                    break
            since_id = tweet.id
    except tweepy.TweepError as error:
            print('\nError. Retweet not successful. Reason: ')
            print(error.reason)
    print("You keep me waiting waiting waiting for an answer")
    time.sleep(30)