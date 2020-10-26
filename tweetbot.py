# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 18:10:56 2018

@author: KalcikR
"""


import tweepy
import labels
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from emojipy import Emoji
from reportlab.lib import colors
import pickle
from PyPDF2 import PdfFileMerger
import sys
import pandas as pd
# sys.path.append("C:/Users/KalcikR/OneDrive/Robert/GitHub/world-control")
# sys.path.append("C:/OneDrive/Robert/GitHub/world-control")
from key import *
from module import *
import os
cwd = os.getcwd()
import traceback
from shutil import copyfile
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

### Register Font

font_file = 'font/Symbola_hint.ttf'
symbola_font = TTFont('Symbola', font_file)
pdfmetrics.registerFont(symbola_font)


from reportlab.lib.pagesizes import A4, landscape
width, height = landscape(A4)
cm = 28.346456692913385
def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y

# TODO batch
# TODO Send email if loop breaks

# "💶".encode('unicode-escape')

# Authenticate
api = create_api("@MinisterVlatin")

with open ('twitter_history', 'rb') as fp:
    twitter_history = pickle.load(fp)

# df = pd.DataFrame.from_csv('master.csv', encoding = "utf-8")
df = pd.read_excel('master.xlsx')

_l = []
# for t in twitter_history:
for t in df['full_text']:
    _l.append(text2paragraph(t))

specs = labels.Specification(297, 210, 5, 5, 59, 38.8, corner_radius=0, top_margin=7.5, left_margin = 1, row_gap = 0.25, column_gap = 0)


# worldcontrol = api.search(q = "@truWorldControl", tweet_mode='extended')
# since_id = worldcontrol[1].id
# since_id = None
since_id = twitter_history[0]['id']


def create_pdf(tweet, _l):
    logger.info("Create PDF")
    # t = process_text(tweet)
    for i in range(0,20):
        while True:
            try: 
                t = text2paragraph(tweet.full_text)
            except:
                continue
            break
    
    _l = _l + [t]
    rev_l = list(reversed(_l))
    cards = [rev_l[0:5],rev_l[5:10],rev_l[10:15],rev_l[15:20],rev_l[20:25]]
    #Create table
    table = Table(cards, 5.9 * cm, 3.88 * cm)
    table.setStyle(TableStyle([
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                            ('VALIGN',(0,0),(-1,-1),'BOTTOM')
                            # ('SIZE', (0,0), (-1,-1), 20)
                            ]))
    canv = canvas.Canvas('front.pdf', pagesize = landscape(A4))
    table.wrapOn(canv, width, height)
    table.drawOn(canv, *coord(0.1, 20.2, cm))
    canv.save()
    # Merge front with back
    merger = PdfFileMerger()
    merger.append('front.pdf')
    merger.append('wc_news_A4_back.pdf')
    merger.write('fakenewz.pdf')
    # upload_pdf(["wc_newz.pdf", "twitter_history", "master.xlsx"], cwd)
    #upload_ftp("fakenewz.pdf", ftp_user, ftp_password)
    copyfile("fakenewz.pdf", "/var/www/html/fakenewz.pdf")

def extend_db(tweet, df, twitter_history):
    logger.info("Extending DB")
    twitter_history.insert(0, tweet._json)
    with open('twitter_history', 'wb') as fp:
            pickle.dump(twitter_history, fp)
    df = df.append(twitter_history[0], ignore_index = True)
    df.to_excel('master.xlsx')

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.search, q='@truWorldControl -filter:retweets', since_id = since_id, tweet_mode='extended').items(): # api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            logger.info("Tweet is a reply")
            continue
        if (tweet.retweeted) or ('RT @' in tweet.full_text):
            logger.info("Tweet is a retweet")
            continue
        # if Minister has not yet responded
        # if any(keyword in tweet.full_text.lower() for keyword in keywords):
        if "#fakenewz" not in tweet.full_text:
            logger.info("Tweet does not contain #fakenewz")
            continue

        if "спасибо" in tweet.full_text:
            logger.info("Caught a response")
            continue

        logger.info(f"Bot found tweet by @{tweet.user.screen_name}. Attempting to respond.")

        if not tweet.user.following and not tweet.user.id == 1017118454711771136:
            tweet.user.follow()
            
        # TODO: Double check that the global df gets altered. Second tweet also includes changes from first?
        extend_db(tweet, df, twitter_history)
        # TODO: Double check that the global _l gets altered. Second tweet also includes changes from first?
        create_pdf(tweet, _l)
        logger.info("Respond")
        m = '@%s спасибо, i‘ll make your „news“ come tru! and so can you: PRINT > world-control.net/pages/latest-newz' % (tweet.user.screen_name)
        api.update_status(m, tweet.id)
    return new_since_id

def main(since_id):
    api = create_api()
    # since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(10)

if __name__ == "__main__":
    main(since_id)