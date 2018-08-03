import tweepy
import labels
from reportlab.graphics import shapes
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red, transparent
import tweepy
from git import Repo
import pandas as pd
import textwrap
import pickle
import unicodedata
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

# drawing = svg2rlg(path + "tank.svg")
#renderPDF.drawToFile(drawing, path + "test.pdf")


print('\U0001f603')

# TODO Hinterseite
# Syntax (Emoji + einfacher Kartentext)
# Autostart try iferror
# module
# batch 
# deploy on rasp py
# store results (on rasp)
# Parse eckige Klammern
# First try while, if it does not work schedule with authentication


# path = "C:/Onedrive/Robert/GitHub/world-control/"
path = "C:/Users/KalcikR/Onedrive/Robert/GitHub/world-control/"

CONSUMER_KEY = 'GKfxpowUC5fzAHCF4FHAyBvgK'
CONSUMER_SECRET = 'abMwFWpqoQ5PBJnt4j5UUyG53pdASJg1y8K7Db3zCe4RTYyZmN'
ACCESS_KEY = '1017118454711771136-fxFqWDnFDPeYg5IiKEemIhsTFNYzCR'
ACCESS_SECRET = 'RhY1IitFjzKNa3v3S02LXlNOPrBRfpklsHdn8325nodit'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


# text = ["Supreme Leader Kim Young Fun has a good day :)", 
# "To show his feelings of joy, a terrifying missile is built & publicly displayed.",
# "PJONG JANG +1"]

# o = [textwrap.wrap(x, 30) for x in text]
# _l = [o]*25
with open (path + 'outfile', 'rb') as fp:
    _l = pickle.load(fp)

_l = worldcontrol

repo = Repo(path)
# fName = 'tweets.txt'     

def upload_pdf(file_list):
    commit_message = 'Add new pdf'
    repo.index.add(file_list)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push('master')

specs = labels.Specification(297, 210, 5, 5, 59, 40, corner_radius=0, top_margin=5, row_gap = 0)

def scale(drawing, scaling_factor):
    """
    Scale a reportlab.graphics.shapes.Drawing()
    object while maintaining the aspect ratio
    """
    scaling_x = scaling_factor
    scaling_y = scaling_factor
 
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing
 

def draw_label(label, width, height, obj):
    i = 90
    for t in obj[0]:
        for r in t:
            label.add(shapes.String(10, i, str(r), fontName="Helvetica", fontSize=9))
            i = i - 10
        i = i - 20
    
    # i = 50
    # for t in obj[1]:
    #    label.add(shapes.String(10, i, str(t), fontName="Helvetica", fontSize=9))
    #    i = i - 10
    
    i = 10
    # for t in obj[2]:
    for t in obj[1]:
        label.add(shapes.String(10, i, str(t), fontName="Helvetica", fontSize=9))
        # label.add(drawing)
        i = i - 10
    
    s = shapes.Rect(5, 8, 150, 11, fill = True)
    s.fillColor = transparent
    label.add(s)


worldcontrol = api.search(q = "@truWorldControl", since_id = since_id)
since_id = worldcontrol[2].id
since_id = None

# t = _l[0] # worldcontrol[0]
# with open(fName, 'w') as f:
def process_text(tweet):
    t = tweet.text.replace("@truWorldControl", "").replace("#fakenewz", "").strip()
    # t = worldcontrol[2].text
    if t.find("[")!=-1:
        desc = t[0:t.find("[")].strip().split("\n")
        desc = [textwrap.wrap(x, 30) for x in desc]
        effect = t[t.find("[")+1:t.find("]")]
        effect = textwrap.wrap(effect, 30)
        r = [desc, effect]
    else:
        text = t.split("\n")[1:4]
        r = [textwrap.wrap(x, 30) for x in text]
    return(r)



import time
while True:
    print("loop")
    for tweet in tweepy.Cursor(api.search, q='@truWorldControl', since_id = since_id).items(5):
        try:
            print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')
            t = process_text(tweet)
            print(t)
            _l = [t] + _l
            sheet = labels.Sheet(specs, draw_label, border=True)
            sheet.add_labels(_l[0:25])
            sheet.save(path + 'world-control.pdf')
            upload_pdf(["world-control.pdf"])
            # tweet.retweet("Hello! Find your card ready for print here: https://github.com/robertkck/world-control/raw/master/world-control.pdf")
            m = "@%s Hello! Find your card ready for print here: https://github.com/robertkck/world-control/raw/master/world-control.pdf" % (tweet.user.screen_name) 
            print(m)
            api.update_status(m, tweet.id)
            with open(path + 'outfile', 'wb') as fp:
                    pickle.dump(_l, fp)
            time.sleep(10)
        except tweepy.TweepError as error:
            print('\nError. Retweet not successful. Reason: ')
            print(error.reason)
        except StopIteration:
            break
    time.sleep(30)



    worldcontrol = api.search(q = "@truWorldControl", since) 
    tweet = worldcontrol[0]
    text = tweet.text.split("\n")[1:4]
    o = [textwrap.wrap(x, 30) for x in text]
    if (o != t):
        print("New Tweet!")
        sheet = labels.Sheet(specs, draw_label, border=True)
        _l = [o] + _l
        sheet.add_labels(_l[0:25])
        sheet.save(path + 'world-control.pdf')
        upload_pdf(["world-control.pdf"])
        m = "@%s Hello! Find your card ready for print here: https://github.com/robertkck/world-control/raw/master/world-control.pdf" % (tweet.user.screen_name) 
        print(m)
        api.update_status(m, tweet.id)
        with open(path + 'outfile', 'wb') as fp:
            pickle.dump(_l, fp)
    time.sleep(30)
    

            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))