# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 19:05:49 2018

@author: rober
"""

import tweepy
from key import *
import pickle

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
    
