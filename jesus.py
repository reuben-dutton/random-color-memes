from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random
import facebook, requests
import json
import numpy as np
import sys
import textwrap
import jesus_supp as js

env = json.loads(open(sys.path[0] + '/env.json').read())
page_id = env['page_id']
acstoke = env['page_token']
graph = facebook.GraphAPI(access_token=acstoke)

colordict = json.loads(open(sys.path[0] + '/json/colordict.json').read())
themes = json.loads(open(sys.path[0] + '/json/themes.json').read())

font70 = ImageFont.truetype(sys.path[0] + "/fonts/Oswald/Oswald-Bold.ttf", 70)
font60 = ImageFont.truetype(sys.path[0] + "/fonts/Oswald/Oswald-Bold.ttf", 60)
font50 = ImageFont.truetype(sys.path[0] + "/fonts/Oswald/Oswald-Bold.ttf", 50)

def conv_HSV(R, G, B):
    RInv = R/255
    GInv = G/255
    BInv = B/255

    Cmax = max(RInv, GInv, BInv)
    Cmin = min(RInv, GInv, BInv)
    delta = Cmax - Cmin

    if delta == 0:
        H = 0
    elif Cmax == RInv:
        H = ((GInv-BInv)/delta) % 6
    elif Cmax == GInv:
        H = ((BInv-RInv)/delta) + 2
    elif Cmax == BInv:
        H = ((RInv-GInv)/delta) + 4

    if Cmax == 0:
        S = 0
    else:
        S = delta/Cmax

    return (H*60, S*100, Cmax*100)

def conv_CMYK(R, G, B):
    RInv = R/255
    GInv = G/255
    BInv = B/255
    K = 1 - max(RInv, GInv, BInv)
    if K == 1:
        return (0, 0, 0, 1)
    else:
        C = (1 - RInv - K)/(1 - K)
        M = (1 - GInv - K)/(1 - K)
        Y = (1 - BInv - K)/(1 - K)
        return (C, M, Y, K)

def conv_HEX(r, g, b):
    return '#%02X%02X%02X' % (r, g, b)

def findStart(middle, text, font):
    return (middle[0] - font.getsize(text)[0]/2,
            middle[1] - font.getsize(text)[1]/2)

def findEnd(middle, text, font):
    return (middle[0] + font.getsize(text)[0]/2,
            middle[1] + font.getsize(text)[1]/2)

def genMessage(R, G, B):

    message = dict()
    message["RGB"] = (R, G, B)
    message["CMYK"] = conv_CMYK(R, G, B)
    message["HSV"] = conv_HSV(R, G, B)
    message["HEX"] = conv_HEX(R, G, B)
    
    ## finding the closest color in terms of RGB
    mindiff = 255*math.sqrt(3)
    colorapprox = ''
    for color, rgb in colordict.items():
        p = [R-rgb[0], G-rgb[1], B-rgb[2]]
        dist = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
        if dist < mindiff:
            mindiff = dist
            message["name"] = color

    if mindiff == 0:
        message["prename"] = 'This is named'
    elif mindiff <= 12:
        message["prename"] = 'Almost identical to'
    elif mindiff <= 25:
        message["prename"] = 'Close to'
    elif mindiff < 50:
        message["prename"] = 'Looks like'

    #generating wavelength approximation
    H = conv_HSV(R, G, B)[0]*60
    message["WAVE"] = -6.173261112*(10**-11)*(H**6) \
    + 5.515102757*(10**-8)*(H**5) \
    - 1.890868343*(10**-5)*(H**4) \
    + 3.063661184*(10**-3)*(H**3) \
    - 0.2277357517*(H**2) \
    + 4.885819756*H + 650

    if not (380 < message["WAVE"] < 720):
        message["WAVE"] = "N/A"
    else:
        message["WAVE"] = '%.2fnm' % message["WAVE"]

    return message

def genPlainColor(R, G, B):
    im = Image.new("RGBA", (2000, 2000), color=0)
    im.paste((R, G, B, 255), (0, 0, 2000, 2000))
    return im

def genTemplateColor(R, G, B):

    msg = genMessage(R, G, B)
    imageSize = (2620, 2000)
    displayStart = 2000
    displayEnd = imageSize[0]
    displayWidth = displayEnd - displayStart
    displaySize = (displayEnd-displayStart, imageSize[1])
    displayMiddle = displaySize[0]/2

    spacesStart = 80
    headingGap = 30
    headingHeight = 80
    spacesSpacing = 250

    brightness = math.sqrt(0.299*R**2 + 0.587*G**2 + 0.114*B**2) / 255
    scale = int(175 + 80*(1-brightness))
    iconcolor = (255, 255, 255, 255)
    coverColor = (scale, scale, scale, 80)
    scaleR = int((10-brightness)*R/10)
    scaleG = int((10-brightness)*G/10)
    scaleB = int((10-brightness)*B/10)
    fontColor = (scaleR, scaleG, scaleB, 255)
    
    baseImage = Image.new("RGBA", imageSize, color=(R, G, B, 255))

    baseDisplay = Image.new("RGBA", displaySize, color=(R, G, B, 255))
    transparentCover = Image.new("RGBA", displaySize, color=coverColor)
    workingDisplay = Image.alpha_composite(baseDisplay, transparentCover)
    canvas = ImageDraw.Draw(workingDisplay)

    spaces = [
        ("RGB",
         '%s, %s, %s' % msg["RGB"]),
        ("CMYK",
         '%.2f, %.2f, %.2f, %.2f' % msg["CMYK"]),
        ("HSV",
         '%.1f° %.1f%% %.1f%%' % msg["HSV"]),
        ("HEX",
         msg["HEX"]),
        ("WAVE",
         msg["WAVE"])
        ]

    for i in range(len(spaces)):
        key, value = spaces[i]
        xDown = spacesSpacing * i + spacesStart
        headingCentre = (displayMiddle,
                         xDown + headingHeight/2)
        headingStart = findStart(headingCentre, key, font60)
        headingEnd = findEnd(headingCentre, key, font60)
        headingEnd = (headingEnd[0], headingEnd[1] + 16)

        arc1 = [(headingStart[0] - headingHeight/2,
                 headingStart[1]),
                (headingStart[0] + headingHeight/2,
                 headingEnd[1])]
        arc2 = [(headingEnd[0] - headingHeight/2,
                 headingStart[1]),
                (headingEnd[0] + headingHeight/2,
                 headingEnd[1])]
                           
        canvas.rectangle([headingStart, headingEnd], fill=iconcolor)
        canvas.pieslice(arc1, 90, 270, fill=iconcolor)
        canvas.pieslice(arc2, 270, 90, fill=iconcolor)
        canvas.text(headingStart, key, font=font60, fill=fontColor)

        valueStart = (displayMiddle-font60.getsize(value)[0]/2,
                      xDown + headingHeight + headingGap)

        canvas.text(valueStart, value, font=font60, fill=iconcolor)

    lines = textwrap.wrap(msg["name"], width=15,
                         break_long_words=False,
                         break_on_hyphens=False)
    
    name = '\n'.join(lines)
    prenameStart = 2000 - len(lines)*100 - 100
    nameStart = 2000 - len(lines)*100

    prenameStart = findStart((displayMiddle, prenameStart), msg["prename"], font50)
    maxline = max(lines, key=len)
    nameStart = findStart((displayMiddle, nameStart), maxline, font70)
    
    canvas.text(prenameStart, msg["prename"], font=font50, fill=iconcolor)
    canvas.multiline_text(nameStart, name, font=font70, fill=iconcolor, spacing=8, align="center")

    baseImage.paste(workingDisplay, (displayStart, 0))
    return baseImage

def retrieve_theme():
    with open(sys.path[0] + "/themes/current.txt", "r") as f:
        themename = f.readline()
    theme = themes[themename]
    result = js.ColorTheme(themename)
    result.importTheme(theme)
    return result
    
def post():
    currenttheme = retrieve_theme()
    R, G, B = currenttheme.getRandom()
    colorTemplate = genTemplateColor(R, G, B)
    colorPlain = genPlainColor(R, G, B)
    theme = "Theme: %s" % currenttheme.getName()
    msg = genMessage(R, G, B)
    msg = '\n'.join([
        "RGB: (%s, %s, %s)" % msg["RGB"],
        "CMYK: (%.2f, %.2f, %.2f, %.2f)" % msg["CMYK"],
        "HSV: %.1f°, %.1f%%, %.1f%%" % msg["HSV"],
        "HEX: %s" % msg["HEX"],
        "WAVELENGTH: %s" % msg["WAVE"],
        "%s %s" % (msg["prename"], msg["name"])
        ])
    print(msg)
    colorTemplate.save(sys.path[0] + '/image.png', 'PNG')
    postid = graph.put_photo(image=open(sys.path[0] + '/image.png', 'rb'), message=theme)['post_id']
    with open(sys.path[0] + '/postids/postids.txt', 'a') as f:
        f.write(str(postid) + '\n')
    colorPlain.save(sys.path[0] + '/image.png', 'PNG')
    graph.put_photo(image=open(sys.path[0] + '/image.png', 'rb'), message = msg, album_path=str(postid) + '/comments')

if __name__ == "__main__":
    post()
