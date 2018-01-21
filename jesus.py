from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random
import facebook, requests
import json
import numpy as np
import sys

env = json.loads(open(sys.path[0] + '/env.json').read())
page_id = env['page_id']
acstoke = env['page_token']
graph = facebook.GraphAPI(access_token=acstoke)

colordict = json.loads(open(sys.path[0] + '/json/colordict.json').read())

def rgb_to_hex(red, green, blue):
    return '#%02X%02X%02X' % (red, green, blue)

def gen_shade(color, brightness, newlight):
    
    RInv = color[0]/255
    GInv = color[1]/255
    BInv = color[2]/255

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
    L = (Cmax + Cmin)/2

    if delta == 0:
        S = 0
    else:
        S = (delta)/(1-math.sqrt((2*L - 1)**2))

    L = newlight
    
    C = (1-math.sqrt((2*L - 1)**2))*S
    X = C*(1 - math.sqrt(((H**2) % 2 - 1)**2))
    m = L - C/2

    if H >= 0 and H < 1:
        color = ((C+m)*255, (X+m)*255, m*255, 255)
    elif H >= 1 and H < 2:
        color = ((X+m)*255, (C+m)*255, m*255, 255)
    elif H >= 2 and H < 3:
        color = (m*255, (C+m)*255, (X+m)*255, 255)
    elif H >= 3 and H < 4:
        color = (m*255, (X+m)*255, (C+m)*255, 255)
    elif H >= 4 and H < 5:
        color = ((C+m)*255, m*255, (X+m)*255, 255)
    elif H >= 5 and H < 6:
        color = ((X+m)*255, m*255, (C+m)*255, 255)

    return (int(color[0]), int(color[1]), int(color[2]), 255)

def gen_color_2(R, G, B):
    im = Image.new("RGBA", (2000, 2000), color=0)
    im.paste((R, G, B, 255), (0, 0, 2000, 2000))
    msg = gen_message(R, G, B, 2)
    return {'image': im, 'message': msg}

def gen_color(R, G, B):
    brightness = math.sqrt(0.299*R**2 + 0.587*G**2 + 0.114*B**2) / 255

    RGB, HEX, HSV, CMYK, WL, AC, ACT = gen_message(R, G, B, 1)

    #fonts for different stats
    font70 = ImageFont.truetype("fonts/Oswald/Oswald-Bold.ttf", 70)
    font55 = ImageFont.truetype("fonts/Oswald/Oswald-Bold.ttf", 55)
    font50 = ImageFont.truetype("fonts/Oswald/Oswald-Bold.ttf", 50)
    font60 = ImageFont.truetype("fonts/Oswald/Oswald-Bold.ttf", 60)
    font100 = ImageFont.truetype("fonts/riffic/RifficFree-Bold.ttf", 100)
    font150 = ImageFont.truetype("fonts/cheeky_rabbit/Cheeky Rabbit.ttf", 150)

    im = Image.new("RGBA", (2525, 2000), color=0)
    im.paste((R, G, B, 255), (0, 0, 2525, 2000))
    infodis = Image.new("RGBA", (2525, 2000), color=0)
    icondis = Image.new("RGBA", (2525, 2000), color=0)
    draw = ImageDraw.Draw(im)
    draw2 = ImageDraw.Draw(infodis)
    draw3 = ImageDraw.Draw(icondis)
    
    if brightness >= 0.74:
        draw2.rectangle((1995, 0, 2525, 2560), fill = (0, 0, 0, 60))
        iconbackcolor = (195, 195, 195, 165)
        fontcolor = gen_shade((R, G, B), brightness, 0.95)
    else:
        draw2.rectangle((1995, 0, 2525, 2560), fill = (255, 255, 255, 25))
        iconbackcolor = (245, 245, 245, 165)
        fontcolor = gen_shade((R, G, B), brightness, 0.9)


    #RGB icon backing
    draw3.rectangle((2215, 80, 2305, 160), fill=iconbackcolor)
    draw3.ellipse((2170, 80, 2250, 160), fill=iconbackcolor)
    draw3.ellipse((2270, 80, 2350, 160), fill=iconbackcolor)
    #CMYK icon backing
    draw3.rectangle((2200, 330, 2320, 410), fill=iconbackcolor)
    draw3.ellipse((2155, 330, 2245, 410), fill=iconbackcolor)
    draw3.ellipse((2285, 330, 2365, 410), fill=iconbackcolor)
    #HSV icon backing
    draw3.rectangle((2215, 565, 2305, 645), fill=iconbackcolor)
    draw3.ellipse((2170, 565, 2250, 645), fill=iconbackcolor)
    draw3.ellipse((2270, 565, 2350, 645), fill=iconbackcolor)
    #HEX icon backing
    draw3.ellipse((2200, 807, 2320, 927), fill=iconbackcolor)
    #WL icon backing
    draw3.ellipse((2200, 1087, 2320, 1207), fill=iconbackcolor)

    
    fim = Image.alpha_composite(im, icondis)
    fim = Image.alpha_composite(fim, infodis)

    drawf = ImageDraw.Draw(fim)

    AC = AC.split(" ")
    length = 0
    tempstring = ''
    linecount = 0
    AC2 = []
    for i in range(len(AC)-1, -1, -1):
        if length + (font70.getsize(AC[i]))[0] > 430:
            AC2.append(tempstring)
            tempstring = AC[i]
            length = 0
        else:
            tempstring = AC[i] + ' ' + tempstring
            length += (font70.getsize(AC[i]))[0]
    AC2.append(tempstring)

    for i in range(len(AC2)):
        height = 1848 - ((font70.getsize(AC2[i])[1] + 5)*(i))
        drawf.text((2260-((font70.getsize(AC2[i])[0] - font70.getsize(' ')[0])/2), height), AC2[i], font=font70, fill=fontcolor)
        
    drawf.text((2260-((font50.getsize(ACT)[0] - font50.getsize(' ')[0])/2), 1848 - ((font70.getsize(AC2[0])[1] + 5)*(len(AC2)))), ACT, font=font50, fill=fontcolor)

    drawf.text((2260-(font70.getsize(RGB)[0]/2), 180), RGB, font=font70, fill=fontcolor)
    drawf.text((2260-(font55.getsize(CMYK)[0]/2), 435), CMYK, font=font55, fill=fontcolor)
    drawf.text((2260-(font50.getsize(HSV)[0]/2), 675), HSV, font=font50, fill=fontcolor)
    drawf.text((2260-(font60.getsize(HEX)[0]/2), 950), HEX, font=font60, fill=fontcolor)
    drawf.text((2260-(font60.getsize(WL)[0]/2), 1230), WL, font=font60, fill=fontcolor)
    
    drawf.text((2262-(font100.getsize('#')[0]/2), 807), '#', font=font100, fill=(R, G, B, 255))
    drawf.text((2261-(font150.getsize('~')[0]/2), 1067), '~', font=font150, fill=(R, G, B, 255))
    drawf.text((2261-(font60.getsize('RGB')[0]/2), 75), 'RGB', font=font60, fill=(R, G, B, 255))
    drawf.text((2261-(font60.getsize('CMYK')[0]/2), 325), 'CMYK', font=font60, fill=(R, G, B, 255))
    drawf.text((2261-(font60.getsize('HSV')[0]/2), 560), 'HSV', font=font60, fill=(R, G, B, 255))
    
    return fim

def gen_message(R, G, B, mode):

    ## finding the closest color in terms of RGB
    mindiff = 255*3
    colorapprox = ''
    for color, rgb in colordict.items():
        p = [R-rgb[0], G-rgb[1], B-rgb[2]]
        dist = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
        if dist < mindiff:
            mindiff = dist
            colorapprox = color

    if mindiff == 0:
        colorapprox2 = 'This is named'
    elif mindiff <= 12:
        colorapprox2 = 'Identical to'
    elif mindiff <= 25:
        colorapprox2 = 'Close to'
    elif mindiff < 50:
        colorapprox2 = 'Looks like'
        
    ## setting up variables for CMYK and HSV conversion
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

    #generating wavelength approximation
    H = H*60
    WL = -6.173261112*(10**-11)*(H**6) \
    + 5.515102757*(10**-8)*(H**5) \
    - 1.890868343*(10**-5)*(H**4) \
    + 3.063661184*(10**-3)*(H**3) \
    - 0.2277357517*(H**2) \
    + 4.885819756*H + 650
    
    if WL > 780:
        WL = 'N/A'
    elif WL < 380:
        WL = 'N/A'
    else:
        WL = '%.2f' % WL
        WL = str(WL) + 'nm'

    if Cmax == 0:
        S = 0
    else:
        S = delta/Cmax

    ## generating HSV
    H = '%.1f' % H
    S = '%.1f' % (S * 100)
    Cmax = '%.1f' % (Cmax * 100)

    if mode == 1:
        HSV = (str(H) + '° ' + str(S) + '% '  + str(Cmax) + '%')
    elif mode == 2:
        HSV = '(' + str(H) + '°, ' + str(S) + '%, '  + str(Cmax) + '%)'

    
    ## generating CMYK
    K = 1 - max(RInv, GInv, BInv)
    if K == 1:
        C = 0.00
        M = 0.00
        Y = 0.00
    else:
        C = (1 - RInv - K)/(1 - K)
        M = (1 - GInv - K)/(1 - K)
        Y = (1 - BInv - K)/(1 - K)
        
    K = '%.2f' % K
    C = '%.2f' % C
    M = '%.2f' % M
    Y = '%.2f' % Y

    ## generating final image
    if mode == 1:
        message = [str(R) + '-' + str(G) + '-' + str(B),
                   str(rgb_to_hex(R, G, B)),
                   HSV,
                   C + ' ' + M + ' ' + Y + ' ' + K,
                   WL,
                   colorapprox, colorapprox2]
    elif mode == 2:
        message = 'RGB: (' + str(R) + ', ' + str(G) + ', ' + str(B) \
        + ')\nHex: ' + str(rgb_to_hex(R, G, B)) \
        + '\nHSV: ' +  HSV \
        + '\nCMYK: (' + str(C) + ', ' + M + ', ' + Y + ', ' + str(K) \
        + ')\n' + 'Approx. wavelength: ' + WL \
        + '\n' + colorapprox2 + ' ' + colorapprox
    return(message)

def post():
    R = random.randrange(0, 256)
    G = random.randrange(0, 256)
    B = random.randrange(0, 256)
    color = gen_color(R, G, B)
    color2 = gen_color_2(R, G, B)
    msg = color2['message']
    color2 = color2['image']
    color.save('image.png', 'PNG')
    graph.put_photo(image=open('image.png', 'rb'), message='')
    f = open(sys.path[0] + '/objectids.txt', 'a')
    postid = graph.get_object('me/feed', limit=1)['data'][0]['id']
    f.write(str(postid) + '\n')
    f.close()
    color2.save('image.png', 'PNG')
    graph.put_photo(image=open('image.png', 'rb'), message = msg, album_path=str(postid) + '/comments')

if __name__ == "__main__":
    post()

