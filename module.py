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
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import simpleSplit
from reportlab.lib.pagesizes import A4, landscape
import ftplib
cm = 28.346456692913385
import emoji_unicode
import emoji
from emojipy import Emoji
import re
from ftplib import FTP


# from googleapiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
# from oauth2client.service_account import ServiceAccountCredentials
# import gspread

# If modifying these scopes, delete the file token.json.
#scope = ['https://spreadsheets.google.com/feeds']
#store = file.Storage('token.json')
#creds = store.get()
#if not creds or creds.invalid:
#    flow = client.flow_from_clientsecrets('credentials.json', scope)
#    creds = tools.run_flow(flow, store)
#service = build('sheets', 'v4', http=creds.authorize(Http()))
#sheet = client.open("fakenewz").sheet1
#SPREADSHEET_ID = '1kHJmRvcfnIW38hbp8wpzbYh7iThsOrf04_C6PbBxhIQ'
#RANGE_NAME = 'Class Data!A2:E'
#result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
#                                            range=RANGE_NAME).execute()
#values = result.get('values', [])
#
## The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#SAMPLE_RANGE_NAME = 'Class Data!A2:E'

font_file = 'font/Symbola_hint.ttf'
# font_file = 'font/NotoSans-Regular.ttf'
# font_file = 'font/NotoEmoji-Regular.ttf'
# font_file = 'font/OpenSansEmoji.ttf'
# open_font = TTFont('OpenSansEmoji', font_file)
# emoji_font = TTFont('Noto Emoji', font_file)
symbola_font = TTFont('Symbola', font_file)
# noto_font = TTFont('Noto Sans', font_file)
pdfmetrics.registerFont(symbola_font)
# pdfmetrics.registerFont(emoji_font)
# pdfmetrics.registerFont(open_font)
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
stylesheet=getSampleStyleSheet()
normalStyle = stylesheet['Normal']

emoji_dict = {
        '1f680':'arms', '1f52b':'arms', '2694':'arms', '1f3f9':'arms', '1f5e1':'arms',
        "1f6e2":"oil",  "26fd":"oil",
        "1f6e9":"air", "2708":"air", "1f6eb":"airstrike", "1f6ec":"airlift",
        "1f480":"skull", "2620":"skull",
        '1f335':'bio', '1f333':'bio', 'f330 ':'bio', 'f95c ':'bio', 'f344 ':'bio', 'f966 ':'bio', 'f952 ':'bio', 'f336 ':'bio', 'f33d ':'bio', 'f955 ':'bio', 'f954 ':'bio', 'f346 ':'bio', 'f951 ':'bio', 'f965 ':'bio', 'f345 ':'bio', 'f95d ':'bio', 'f353 ':'bio', 'f352 ':'bio', 'f351 ':'bio', 'f350 ':'bio', 'f34f ':'bio', 'f34e ':'bio', 'f34d ':'bio', 'f34c ':'bio', 'f34b ':'bio', 'f34a ':'bio', 'f349 ':'bio', 'f348 ':'bio', 'f347 ':'bio',
        '1f3c6':'gold', '1f947':'gold', '1f3c5':'gold', '1f396':'gold', '1f3f5':'gold', '1f4b0':'gold', '1f48e':'gold',
        '1f48a':'chem', '2697':'chem', '1f321':'chem', '1f489':'chem', '2623':'chem', '2622':'chem',
        '1f579':'tech', '1f4f1':'tech', '1f4f2':'tech', '1f4be':'tech', '1f4bd':'tech', '1f4bb':'tech', '1f39a':'tech', '2699':'tech', 'fe0f':'tech',
        '1f468-200d-1f393':'sage', '1f469-200d-1f393':'sage', '1f9d9-200d-2642':'sage', '1f9d9-200d-2640':'sage','1f535':'sage',
        '1f534':'general', '1f468-200d-2708':'general', '1f469-200d-2708':'general', '1f46e':'general',
        '1f4b2':'yollo', '1f4b4':'yollo', '1f4b3':'yollo', '1f4b6':'yollo', '1f4b7':'yollo', '1f4b5':'yollo', '1f4b8':'yollo',
        '1f468-200d-1f468-200d-1f466-200d-1f466':'corpz', '1f690':'corpz', '1f463':'corpz', '1f691':'corpz', '1f69b':'corpz', '1f697':'corpz', '1f68c':'corpz', '1f69a':'corpz', '1f68d':'corpz', '1f68e':'corpz'
}



#def fetch_sheet():
#    """Shows basic usage of the Sheets API.
#    Prints values from a sample spreadsheet.
#    """
#    store = file.Storage('token.json')
#    creds = store.get()
#    if not creds or creds.invalid:
#        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
#        creds = tools.run_flow(flow, store)
#    service = build('sheets', 'v4', http=creds.authorize(Http()))
#
#    # Call the Sheets API
#    SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#    RANGE_NAME = 'Class Data!A2:E'
#    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
#                                                range=RANGE_NAME).execute()
#    values = result.get('values', [])
#
#    if not values:
#        print('No data found.')
#    else:
#        print('Name, Major:')
#        for row in values:
#            # Print columns A and E, which correspond to indices 0 and 4.
#            print('%s, %s' % (row[0], row[4]))


def upload_pdf(file_list, repo_path):
    # Use ftp instead
    # session = ftplib.FTP('example.com','username','password')
    # file = open('cup.mp4','rb')                  # file to send
    # session.storbinary('STOR '+'cup.mp4', file)     # send the file
    # file.close()                                    # close file and FTP
    # session.quit()
    repo = Repo(repo_path)
    commit_message = 'Add new pdf'
    repo.index.add(file_list)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push('master')

def upload_ftp(filename, ftp_user, ftp_password):
    #domain name or server ip:
    ftp = FTP('files.000webhost.com')
    ftp.login(user=ftp_user, passwd = ftp_password)
    ftp.storbinary('STOR '+ 'public_html/web/' + filename, open(filename, 'rb'))
    ftp.quit()

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
#def process_text(tweet):
#    t = tweet.text.replace("@truWorldControl", "").replace("#fakenewz", "").strip()
#    # t = worldcontrol[2].text
#    if t.find("[")!=-1:
#        desc = t[0:t.find("[")].strip().split("\n")
#        desc = [textwrap.wrap(x, 30) for x in desc]
#        effect = t[t.find("[")+1:t.find("]")]
#        effect = textwrap.wrap(effect, 30)
#        r = [desc, effect]
#    else:
#        text = t.split("\n")[1:4]
#        r = [textwrap.wrap(x, 30) for x in text]
#    return(r)

def text2paragraph(text):
    #TODO If you dont find an effect, still work on the description
    #TODO Icons can also be mentioned in the description --> No because Golden would change to emoji
    font_file = 'font/Symbola_hint.ttf'
    # font_file = 'font/NotoSans-Regular.ttf'
    # font_file = 'font/NotoEmoji-Regular.ttf'
    # font_file = 'font/OpenSansEmoji.ttf'
    # open_font = TTFont('OpenSansEmoji', font_file)
    # emoji_font = TTFont('Noto Emoji', font_file)
    symbola_font = TTFont('Symbola', font_file)
    # noto_font = TTFont('Noto Sans', font_file)
    pdfmetrics.registerFont(symbola_font)
    # pdfmetrics.registerFont(emoji_font)
    # pdfmetrics.registerFont(open_font)
    # t = text.replace("@truWorldControl", "").replace("#fakenewz", "").strip()
    t = text
    t = re.sub("(?i)@truworldcontrol", "", t)
    t = re.sub("(?i)#fakenewz", "", t)
    t = t.strip()
    # t = worldcontrol[2].text
    lines = simpleSplit(t, 'Helvetica', 12, 6.5*cm)
    lineSpacing = 3.88*cm/(len(lines)) - 3

    style_desc = getSampleStyleSheet()
    style_desc = style_desc["BodyText"]
    style_desc.alignment = TA_LEFT
    # style_desc.fontName = 'Noto Emoji'
    # style_desc.spaceAfter = 30
    style_desc.leading = lineSpacing

    style_effect = getSampleStyleSheet()
    style_effect = style_effect["BodyText"]
    # style_effect.fontSize = 16
    # style_effect.fontName = 'Noto Emoji'
    style_effect.borderPadding = 2
    style_effect.alignment = TA_CENTER
    style_effect.borderWidth = 1
    style_effect.borderColor = '#000000'

    # effect = re.search("\[(.*?)\]", t)
    r = []
    p_desc = []
    p_effect = []

    # Needs to be refactored

    if t.find("[")!=-1:
        desc = t[0:t.find("[")].strip()
        effect = t[t.find("[")+1:t.find("]")]
        effect_emoji = replace_emoji(effect, style_effect)
        effect_emoji = effect_emoji.replace("\n", "<br />")
        p_effect = Paragraph(effect_emoji, style_effect)
    else:
        desc = t

    desc = replace_with_emoji(desc, style_desc.fontSize)
    if desc.find("\n")!=-1:
        d = desc.split("\n")
        d[0] = "<u>" + d[0] + "</u>"
        desc = "<br />".join(d)

    p_desc = Paragraph(desc, style_desc)

    r.append(p_desc)
    if p_effect:
        r.append(p_effect)

    return(r)

def replace_emoji(effect, style):
    # t = text.encode('unicode-escape')
    # Würfel Icon
    # Figure icon
    # Alle bauen/roten icons für general/sage
    # Replace text
    # TODO Case insensitive

    effect = effect.replace("<", u"<img src='images/arrow_left.png' valign='middle' width = '15' height = '15' />")
    effect = effect.replace("&lt;", u"<img src='images/arrow_left.png' valign='middle' width = '15' height = '15' />")
    effect = effect.replace("&LT;", u"<img src='images/arrow_left.png' valign='middle' width = '15' height = '15' />")

    effect = effect.replace(">", u"<img src='images/arrow_right.png' valign='middle' width = '15' height = '15' />")
    effect = effect.replace("&gt;", u"<img src='images/arrow_right.png' valign='middle' width = '15' height = '15' />")
    effect = effect.replace("&GT;", u"<img src='images/arrow_right.png' valign='middle' width = '15' height = '15' />")

    icon = ['arms', 'oil', 'airlift', 'airstrike', 'skull', 'bio', 'gold', 'chem', 'tech', 'sage', 'general', 'yollo', 'corpz']
    for i in icon:
        effect = re.sub("(?i)" + i, i, effect)
        if effect.find(i)!=-1:
            effect = effect.replace(i, u"<img src='images/{filename}.png' valign='middle' width = '20' height = '20' />".format(filename = i))

    try:
        t = emoji_unicode.replace(
            effect,
            # lambda e: u"<img src='images/{filename}.svg' valign='middle' width = '20' height = '20' alt= '{raw}' />".format(filename=emoji_dict[e.code_points], raw=e.unicode)
            lambda e: u"<img src='images/{filename}.png' valign='middle' width = '20' height = '20' />".format(filename=emoji_dict[e.code_points])
        )
    except KeyError:
        print("Key Error")
#        t = emoji_unicode.replace(
#            text,
#            # lambda e: u"<img src='images/{filename}.svg' valign='middle' width = '20' height = '20' alt= '{raw}' />".format(filename=emoji_dict[e.code_points], raw=e.unicode)
#            lambda e: u"<font name=Symbola>{raw}</font>".format(raw=e.unicode)
#        )
        # t = replace_with_emoji_pdf(Emoji.to_image(text), style.fontSize)
        t = replace_with_emoji(effect, style.fontSize)
    return(t)

# Pdf doesn't need any unicode inside <image>'s alt attribute
Emoji.unicode_alt = False


def replace_with_emoji(effect, size):
    """
    Reportlab's Paragraph doesn't accept normal html <image> tag's attributes
    like 'class', 'alt'. Its a little hack to remove those attrbs
    """
    e = ""
    for i, c in enumerate(effect):
        if c in emoji.UNICODE_EMOJI:
            e += Emoji.to_image(c)
        else:
            e += c
    e = e.replace('class="emojione " style="" ', 'height=%s width=%s' %
                        (size, size))
    return re.sub('alt="'+Emoji.shortcode_regexp+'"', '', e)

def print_emoji_dict(emoji_dict = emoji_dict):
    for i in emoji_dict:
        for j in i.split('-'):
            print(chr(int(j, 16)))
            # sval("u" + "'{}'".format(n))
