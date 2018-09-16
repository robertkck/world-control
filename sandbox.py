from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from emojipy import Emoji
from reportlab.lib import colors
import re
from module import *

import numpy as np
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape, cm
width, height = landscape(A4)

styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleN.borderWidth = 1
styleN.borderColor = '#000000'

def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y

# Texts
content = "It's emoji time <img src='images/air.png' valign='middle' width = '20' height = '20' /> \U0001F61C. Let's add some cool emotions \U0001F48F \u270C. And some more \u2764 \U0001F436"
print(content)
# styles["Title"].fontName = 'Helvetica'
# style = styles["Title"]
# content = replace_with_emoji_pdf(Emoji.to_image(pdf_content), style.fontSize)

p = Paragraph(content, styleN)
# p = Paragraph('long paragraph', styleN)

ps = []
ps.append(p)
ps.append(p)

data= [[p,p,p,p,p]]*5

# data = np.reshape()

table = Table(data, 5.9 * cm, 3.88 * cm)

table.setStyle(TableStyle([
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))




canv = canvas.Canvas('emoji.pdf', pagesize = landscape(A4))

# para.wrap(width, height)
# para.drawOn(canv, 0, height/2)

table.wrapOn(canv, width, height)
table.drawOn(canv, *coord(0.1, 20, cm))

canv.save()


#######

