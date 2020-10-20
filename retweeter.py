# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 19:05:49 2018

@author: rober
"""

import tweepy
import logging
from key import *
from module import *
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not "@truWorldControl" and "#fakenewz" in tweet.text:
            # Only retweet if both keywords are present. 
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["@truWorldControl", "#fakenewz"])


# worldcontrol = api.search(q = "@truWorldControl", tweet_mode='extended')
# since_id = worldcontrol[1].id
                       
# import time
# while True:
#     print("loop")
#     try:
#         new_tweets = api.search(q = "@truWorldControl", since_id = since_id, tweet_mode='extended')
#         if not new_tweets:
#             print("No new tweet")
#         else:
#             for tweet in tweepy.Cursor(api.search, q='@truWorldControl', since_id = since_id, tweet_mode='extended').items(5):
#                 print("new tweet found: " + tweet.full_text)
#                 try:
#                     if "#fakenewz" not in tweet.full_text:
#                         print("Tweet does not include the #fakenewz Hashtag")
#                     else:
#                         print('\nBot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to respond.')
#                         tweet.retweet()
#                         print('Retweet published successfully.')
#                 except tweepy.TweepError as error:
#                     print('\nError. Retweet not successful. Reason: ')
#                     print(error.reason)
#                 except StopIteration:
#                     break
#             since_id = tweet.id
#     except tweepy.TweepError as error:
#             print('\nError. Retweet not successful. Reason: ')
#             print(error.reason)
#     print("You keep me waiting waiting waiting for an answer")
#     time.sleep(30)