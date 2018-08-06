# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:07:43 2018

@author: KalcikR
"""

from git import Repo
import textwrap
from reportlab.graphics import shapes
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red, transparent


def upload_pdf(file_list, repo_path):
    repo = Repo(repo_path)
    commit_message = 'Add new pdf'
    repo.index.add(file_list)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push('master')

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