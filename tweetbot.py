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
# sys.path.append("C:/Users/KalcikR/OneDrive/Robert/GitHub/world-control")
# sys.path.append("C:/OneDrive/Robert/GitHub/world-control")
from key import *
from module import *
import os
cwd = os.getcwd()
from reportlab.lib.pagesizes import A4, landscape, cm
width, height = landscape(A4)

def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y

# TODO
# Syntax (Emoji + einfacher Kartentext)
# Autostart try iferror
# module
# batch 
# deploy on rasp py
# store results (on rasp)
# First try while, if it does not work schedule with authentication
# Scale Font size
# Set up font with special characters
# Default set of cards
# Change URL to world-control.net
# Send email if loop breaks


# path = "C:/Onedrive/Robert/GitHub/world-control/"
# path = "C:/Users/KalcikR/Onedrive/Robert/GitHub/world-control/"

# Load font
ttfFile = 'font/icomoon.ttf'
pdfmetrics.registerFont(TTFont("icomoon", ttfFile)) 

# Authenticate bo
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


with open ('outfile', 'rb') as fp:
    _l = pickle.load(fp)

with open ('twitter_history', 'rb') as fp:
    twitter_history = pickle.load(fp)

specs = labels.Specification(297, 210, 5, 5, 59, 38.8, corner_radius=0, top_margin=7.5, left_margin = 1, row_gap = 0.25, column_gap = 0)


worldcontrol = api.search(q = "@truWorldControl")
# since_id = worldcontrol[1].id
# since_id = None
since_id = twitter_history[0]['id']

# twitter_history = []
import time
while True:
    print("loop")
    new_tweets = api.search(q = "@truWorldControl", since_id = since_id)
    if not new_tweets:
        print("No new tweet")
    else:
        for tweet in tweepy.Cursor(api.search, q='@truWorldControl', since_id = since_id).items(5):
            print("new tweet found: " + tweet.text)
            twitter_history.insert(0, tweet._json)
            with open('twitter_history', 'wb') as fp:
                    pickle.dump(twitter_history, fp)
            try:
                if "#fakenewz" not in tweet.text:
                    print("Tweet does not include the #fakenewz Hashtag")
                else:
                    print('\nBot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to respond.')
                    # t = process_text(tweet)
                    t = text2paragraph(tweet.text)
                    _l = [t] + _l
                    #sheet = labels.Sheet(specs, draw_label, border=True)
                    #sheet.add_labels(_l[0:25])
                    #sheet.save('front.pdf')
                    cards = [_l[0:5],_l[5:10],_l[10:15],_l[15:20],_l[20:25]]
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
                    table.drawOn(canv, *coord(0.1, 20, cm))
                    canv.save()
                    # Merge front with back
                    merger = PdfFileMerger()
                    merger.append('front.pdf')
                    merger.append('wc_news_A4_back.pdf')
                    merger.write('world-control.pdf')
                    upload_pdf(["world-control.pdf"], cwd)
                    # tweet.retweet("Hello! Find your card ready for print here: https://github.com/robertkck/world-control/raw/master/world-control.pdf")
                    m = "@%s Hello! Find your card ready for print here: https://github.com/robertkck/world-control/raw/master/world-control.pdf" % (tweet.user.screen_name) 
                    print(m)
                    api.update_status(m, tweet.id)
                    with open('outfile', 'wb') as fp:
                            pickle.dump(_l, fp)
                    time.sleep(10)
            except tweepy.TweepError as error:
                print('\nError. Retweet not successful. Reason: ')
                print(error.reason)
            except StopIteration:
                break
        since_id = twitter_history[0]['id']
    print("You keep me waiting waiting waiting for an answer")
    time.sleep(30)