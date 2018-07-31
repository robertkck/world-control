# -*- coding: utf-8 -*-

import labels
from reportlab.graphics import shapes
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red, transparent
import tweepy
from git import Repo
import pandas as pd
import textwrap

path = "C:/Onedrive/Robert/GitHub/world-control/"
styles = getSampleStyleSheet()

def create_labels(text):
  print("Hello from a function") 

default_text = [
["Something", "and", "Something"], ["Something", "and", "Something"], ["Something", "and", "Something"]]

# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(297, 210, 5, 5, 59, 40, corner_radius=0, top_margin=5, row_gap = 0)

# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
                                     
def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    i = 90
    for t in obj[0]:
        label.add(shapes.String(10, i, str(t), fontName="Helvetica", fontSize=9))
        i = i - 10
    
    i = 50
    for t in obj[1]:
        label.add(shapes.String(10, i, str(t), fontName="Helvetica", fontSize=9))
        i = i - 10
    
    i = 10
    for t in obj[2]:
        label.add(shapes.String(10, i, str(t), fontName="Helvetica", fontSize=9))
        i = i - 10
    
    s = shapes.Rect(5, 8, 150, 11, fill = True)
    s.fillColor = transparent
    label.add(s)

# Create the sheet.
sheet = labels.Sheet(specs, draw_label, border=True)

# Add a couple of labels.

text = ["Supreme Leader Kim Young Fun has a good day :)", 
"To show his feelings of joy, a terrifying missile is built & publicly displayed.",
"PJONG JANG +1"]

o = [textwrap.wrap(x, 30) for x in text]
_l = [o]*25

# sheet.add_label(o)
# sheet.add_label("World Control")

# We can also add each item from an iterable.
sheet.add_labels(_l)

# Note that any oversize label is automatically trimmed to prevent it messing up
# other labels.
# sheet.add_label("Oversized label here")

# Save the file and we are done.
sheet.save(path + 'basic.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))

# Upload to github

repo = Repo(path) 
file_list = [
    'basic.pdf'
]
commit_message = 'Add new pdf'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push('master')
# Downloadable at https://github.com/robertkck/world-control/raw/master/basic.pdf

auth = tweepy.OAuthHandler("ayGzE6WOvZf5vLGTd5lrLpMes", "HscCoFzBB29nABNc69OIuLXWK6tigib9KPkfbP4gBxV7pvsbyo")
auth.set_access_token("3929637676-UxwEFtaVR9dTLP5ZRyDdQMMOs0jwxyivsyFcuAZ", "fnEQ7JMF5yHZ7IfrYYpW9dxh4okXW7aCpvEpwERAd70V3")

api = tweepy.API(auth)

public_tweets = api.home_timeline()
worldcontrol = api.search(q = "@truWorldControl")
for tweet in worldcontrol:
    print(tweet.text)

worldcontrol