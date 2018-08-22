# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:07:43 2018

@author: KalcikR
"""

from git import Repo
import textwrap
from reportlab.graphics import shapes
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red, transparent
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import simpleSplit 
from reportlab.lib.pagesizes import A4, landscape, cm
import emoji_unicode
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
stylesheet=getSampleStyleSheet()
normalStyle = stylesheet['Normal']

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
    #  + ' <img src="images/air.png" valign="middle"/>',
    i = 90
    for t in obj[0]:
        for r in t:
            label.add(shapes.String(10, i, str(r), fontName="Helvetica", fontSize=9))
            p = Paragraph("lol", normalStyle)
            i = i - 10
        i = i - 20
    
    # i = 50
    # for t in obj[1]:
    #    label.add(shapes.String(10, i, str(t), fontName="Helvetica", fontSize=9))
    #    i = i - 10
    
    i = 10
    # for t in obj[2]:
    for t in obj[1]:
        label.add(shapes.String(10, i, '<b>' + str(t) + '</b>', fontName="Helvetica", fontSize=9))
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
    
def text2paragraph(text):
    t = text.replace("@truWorldControl", "").replace("#fakenewz", "").strip()
    # t = worldcontrol[2].text
    lines = simpleSplit(t, 'Helvetica', 12, 5.9*cm)
    lineSpacing = 3.88*cm/(len(lines)) - 3
    
    style_desc = getSampleStyleSheet()
    style_desc = style_desc["BodyText"]
    style_desc.alignment = TA_LEFT
    # style_desc.spaceAfter = 30
    style_desc.leading = lineSpacing
    
    style_effect = getSampleStyleSheet()
    style_effect = style_effect["BodyText"]
    # style_effect.fontSize = 16
    style_effect.borderPadding = 2
    style_effect.alignment = TA_CENTER
    style_effect.borderWidth = 1
    style_effect.borderColor = '#000000'
    
    
    if t.find("[")!=-1:
        desc = t[0:t.find("[")].strip()
        if desc.find("\n")!=-1:
            d = desc.split("\n")
            d[0] = "<u>" + d[0] + "</u>"
            desc = "<br />".join(d)
        effect = t[t.find("[")+1:t.find("]")]
        effect = replace_emoji(effect)
        
        p_desc = Paragraph(desc, style_desc)
        p_effect = Paragraph(effect, style_effect)
        
        r = []
        r.append(p_desc)
        r.append(p_effect)
        
    else:
        r = Paragraph(t, style_desc)
    return(r)
    
def replace_emoji(text):
    # t = text.encode('unicode-escape')
    emoji_dict = {"1f34c":"arms", "SOUTH":"S" }
    try:
        t = emoji_unicode.replace(
            text,
            # lambda e: u"<img src='images/{filename}.svg' valign='middle' width = '20' height = '20' alt= '{raw}' />".format(filename=emoji_dict[e.code_points], raw=e.unicode)
            lambda e: u"<img src='images/{filename}.png' valign='middle' width = '20' height = '20' />".format(filename=emoji_dict[e.code_points])
        )
    except KeyError:
        t = text
    return(t)



