# -*- coding: utf-8 -*-

import labels
from reportlab.graphics import shapes
import tweepy
from git import Repo

# path = "C:/Users/KalcikR/OneDrive/Robert/GitHub/world-control/"
path = "C:/Onedrive/Robert/GitHub/world-control/"
print(path)

# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(297, 210, 5, 5, 59, 40, corner_radius=0)

# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    label.add(shapes.String(2, 2, str(obj), fontName="Helvetica", fontSize=40))

# Create the sheet.
sheet = labels.Sheet(specs, draw_label, border=True)

# Add a couple of labels.
sheet.add_label("Hello")
sheet.add_label("World")

# We can also add each item from an iterable.
sheet.add_labels(range(3, 25))

# Note that any oversize label is automatically trimmed to prevent it messing up
# other labels.
sheet.add_label("Oversized label here")

# Save the file and we are done.
sheet.save(path + 'basic.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))



auth = tweepy.OAuthHandler("ayGzE6WOvZf5vLGTd5lrLpMes", "HscCoFzBB29nABNc69OIuLXWK6tigib9KPkfbP4gBxV7pvsbyo")
auth.set_access_token("3929637676-UxwEFtaVR9dTLP5ZRyDdQMMOs0jwxyivsyFcuAZ", "fnEQ7JMF5yHZ7IfrYYpW9dxh4okXW7aCpvEpwERAd70V3")

api = tweepy.API(auth)

public_tweets = api.home_timeline()
worldcontrol = api.search(q = "@truWorldControl")
for tweet in worldcontrol:
    print(tweet.text)

worldcontrol