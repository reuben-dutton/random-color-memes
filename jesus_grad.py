from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random
import facebook, requests
import json
import numpy as np
import sys
import textwrap
import jesus_supp as js

'''
    This file contains the main mechanisms for posting to the
    facebook page. It creates the images as well as calculates
    the relevant information regarding the random color.
'''

# Import the details for the page and link to the Facebook API.
env = json.loads(open(sys.path[0] + '/env.json').read())
page_id = env['page_id']
_access_token = env['page_token']
graph = facebook.GraphAPI(access_token=_access_token)

# Import the color dictionary and themes files.
colors = json.loads(open(sys.path[0]+'/json/colordict.json').read())
themes = json.loads(open(sys.path[0]+'/json/themes.json').read())

# Create different sized fonts for use later.
font_path = "/fonts/Oswald/Oswald-Bold.ttf"
font70 = ImageFont.truetype(sys.path[0] + font_path, 70)
font60 = ImageFont.truetype(sys.path[0] + font_path, 60)
font50 = ImageFont.truetype(sys.path[0] + font_path, 50)

def convert_hsv(r, g, b):
    '''
        Converts a color in RGB format to HSV format.

        Args:
            r: The red content of the color.
            g: The green content of the color.
            b: The blue content of the color.

        Returns:
            A tuple containing the hue, shade and value
            of the given color.
    '''
    # Scale the r, g, b values between 0 and 1.
    r_inv = r/255
    g_inv = g/255
    b_inv = b/255

    # Find the maximum and minimum value, and the
    # difference between the two.
    c_max = max(r_inv, g_inv, b_inv)
    c_min = min(r_inv, g_inv, b_inv)
    delta = c_max - c_min

    # Calculate the hue value scaled from 0 to 6.
    if delta == 0:
        h = 0
    elif c_max == r_inv:
        h = ((g_inv-b_inv)/delta) % 6
    elif c_max == g_inv:
        h = ((b_inv-r_inv)/delta) + 2
    elif c_max == b_inv:
        h = ((r_inv-g_inv)/delta) + 4

    # Calculate the shade value scaled from 0 to 1.
    if c_max == 0:
        s = 0
    else:
        s = delta/c_max

    # Return the values scaled properly (to degrees and percentage).
    return (h*60, s*100, c_max*100)

def convert_cmyk(r, g, b):
    '''
        Converts a color in the RGB color space to one in the
        CMYK color space.

        Args:
            r: The red content of the color.
            g: The green content of the color.
            b: The blue content of the color.

        Returns:
            A tuple containing the cyan, magenta, yellow and
            key content of the given color.
    '''

    # Scale the r, g, b values between 0 and 1.
    r_inv = r/255
    g_inv = g/255
    b_inv = b/255

    # Find the key content of the color.
    k = 1 - max(r_inv, g_inv, b_inv)

    # Find the cyan, magenta and yellow content of
    # the color and return.
    if k == 1:
        return (0, 0, 0, 1)
    else:
        c = (1 - r_inv - k)/(1 - k)
        m = (1 - g_inv - k)/(1 - k)
        y = (1 - b_inv - k)/(1 - k)
        return (c, m, y, k)

def convert_hex(r, g, b):
    ''' Converts the color from rgb to a hex value '''
    return '#%02X%02X%02X' % (r, g, b)

def findStart(middle, text, font):
    ''' Finds the start of a text given the desired
        centre of the text and text size.
    '''
    return (middle[0] - font.getsize(text)[0]/2,
            middle[1] - font.getsize(text)[1]/2)

def findEnd(middle, text, font):
    ''' Finds the end of a text given the desired
        centre of the text and text size.
    '''
    return (middle[0] + font.getsize(text)[0]/2,
            middle[1] + font.getsize(text)[1]/2)

def genMessage(r, g, b):
    '''
        Generates a message describing the various aspects
        of a color given its position in the RGB color space.

        Args:
            r: The red content of the color.
            g: The green content of the color.
            b: The blue content of the color.

        Returns:
            A dictionary containing:
                The RGB value of the color.
                The CMYK value of the color.
                The HSV values of the color.
                The hexadecimal representation of the color.
                The name of the (named) color it is closest to
                visually in the RGB color space.
                A flavor string describing how close it is to
                the aforementioned color.
                The distance between the color and the closest
                named color.
                The approximate wavelength of the color.
    '''

    # Create the dictionary and add RGB, CMYK, HSV and hex.
    message = dict()
    message["RGB"] = (r, g, b)
    message["CMYK"] = convert_cmyk(r, g, b)
    message["HSV"] = convert_hsv(r, g, b)
    message["HEX"] = convert_hex(r, g, b)
    
    # Find the closest color in the RGB color space.
    # Then, add the closest color to the dictionary.
    min_diff = 255*math.sqrt(3)
    for color, rgb in colors.items():
        p = [r-rgb[0], g-rgb[1], b-rgb[2]]
        dist = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
        if dist < min_diff:
            min_diff = dist
            message["name"] = color

    # Adding the distance as 'delta' (will be used in later versions)
    message["delta"] = "%.2f" % min_diff

    # Add an appropriate flavor string to the dictionary.
    if min_diff == 0:
        message["prename"] = 'This is named'
    elif min_diff <= 12:
        message["prename"] = 'Almost identical to'
    elif min_diff <= 25:
        message["prename"] = 'Close to'
    elif min_diff < 50:
        message["prename"] = 'Looks like'
        
    # Generate the wavelength approximation. This is done
    # through some formula I made a while ago and relies on
    # the hue of the color in the HSV color space.
    h = convert_hsv(r, g, b)[0]
    approx_wavelength = -6.173261112*(10**-11)*(h**6) \
    + 5.515102757*(10**-8)*(h**5) \
    - 1.890868343*(10**-5)*(h**4) \
    + 3.063661184*(10**-3)*(h**3) \
    - 0.2277357517*(h**2) \
    + 4.885819756*h + 650

    # If the color is 'outside' the visible spectrum then just
    # remove the approximate wavelength (set it to N/A).
    if not (380 < approx_wavelength < 720):
        message["WAVE"] = "N/A"
    else:
        message["WAVE"] = '%.2fnm' % approx_wavelength

    # Return the dictionary.
    return message

def genPlainColor(colors):
    ''' Return a plain version of the given color as an image. '''
    # Create a new image with the given color.
    start = colors[0]
    end = colors[1]
    plain_color = Image.new("RGBA", (2000, 2000), color=(0, 0, 0, 255))
    canvas = ImageDraw.Draw(plain_color)

    for i in range(2000):
        r = start[0] + int(((end[0] - start[0]) / 2000) * i)
        g = start[1] + int(((end[1] - start[1]) / 2000) * i)
        b = start[2] + int(((end[2] - start[2]) / 2000) * i)
        coords = [i, 0, i, 2000]
        canvas.line(coords, fill=(r, g, b, 255))
    
    # Return the new image.
    return plain_color


def genTemplateColor(colors):
    '''
        Create a picture of the given color along with a sidebar
        showing useful information about that color (including
        positions in various color spaces and some trivia such as
        approximate wavelength and similiar color names.

        Args:
            r: The red content of the color.
            g: The green content of the color.
            b: The blue content of the color.

        Returns:
            Returns a PIL image object of the color along with
            a sidebar containing information about that color.
    '''

    # Create a dictionary containing all the relevant information to
    # be displayed alongside the image.

    # The image's size
    image_size = (3240, 2000)
    offset = 0

    # Create a new image with the given color.
    start = colors[0]
    end = colors[1]
    base_image = Image.new("RGBA", image_size, color=(0, 0, 0, 255))
    r, g, b = start
    color1 = Image.new("RGBA", (620, 2000), color=(r, g, b, 255))
    r, g, b = end
    color2 = Image.new("RGBA", (620, 2000), color=(r, g, b, 255))
    inter = genPlainColor(colors)

    base_image.paste(color1, (0, 0))
    base_image.paste(color2, (2620, 0))
    base_image.paste(inter, (620, 0))

    for color in colors:
        r, g, b = color
        msg = genMessage(r, g, b)

        # The x coordinate at which the information display starts.
        display_start = 2620 * offset
        offset += 1

        # The x coordinate at which the information display ends.
        # (This is the same as the end of the image).
        display_end = display_start + 620

        # The width of the display
        display_width = display_end - display_start

        # A tuple containing the width and length of the display.
        display_size = (display_end - display_start, image_size[1])

        # The length of one half of the display width-wise.
        display_middle = display_size[0] / 2

        # Initialising some important values regarding the information
        # display. 'Spaces' refers to all information excepting closest
        # color name and its associated flavor text.
        # Pieces of information are given a heading which is placed
        # above them. Each piece of information in the 'Spaces' is like
        # this.

        # The y coordinate at which the 'Spaces' information begins.
        spaces_start = 80

        # The distance between the heading for a piece of info and the
        # actual info
        heading_gap = 30

        # The height of the heading.
        heading_height = 80

        # The distance between the the start of two vertically adjacent
        # pieces of information.
        spaces_spacing = 250

        # The following section calculates the icon, cover and font
        # colors to be used in the information display.

        # Calculate the brightness of the given color (from 0 to 1).
        brightness = math.sqrt(0.299*r**2 + 0.587*g**2 + 0.114*b**2) / 255

        # The brighter the color, the darker the cover and vice versa.
        scale = int(175 + 80*(1-brightness))
        icon_color = (255, 255, 255, 255)
        cover_color = (scale, scale, scale, 80)
        scale_r = int((10-brightness)*r/10)
        scale_g = int((10-brightness)*g/10)
        scale_b = int((10-brightness)*b/10)
        # The brighter the color, the darker the font and vice versa.
        font_color = (scale_r, scale_g, scale_b, 255)

        # Create an image for the display with a semi-transparent cover
        # pasted on top and a new canvas object. This canvas object will
        # be used to place the information on top of the working_display.
        base_display = Image.new("RGBA", display_size, color=(r, g, b, 255))
        transparent_cover = Image.new("RGBA", display_size, color=cover_color)
        working_display = Image.alpha_composite(base_display, transparent_cover)
        display_canvas = ImageDraw.Draw(working_display)

        # Create a list containing tuples of the info headings and the
        # respective information.
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

        # Loop through all the relevant information and paste it onto
        # the display in order.
        for i in range(len(spaces)):
            # Retrieve heading and information.
            key, value = spaces[i]
            # Calculate how far down the information is.
            x_down = spaces_spacing * i + spaces_start

            # Create the ellipse containing the heading by pasting
            # two semicircles and a rectangle in the correct place.

            # Calculate the position of the rectangle depending on
            # the size of the heading's text in regards to font.
            heading_centre = (display_middle,
                             x_down + heading_height/2)
            heading_start = findStart(heading_centre, key, font60)
            heading_end = findEnd(heading_centre, key, font60)
            heading_end = (heading_end[0], heading_end[1] + 16)

            # Calculate the position of the two semicircles on either
            # side of the rectangle.
            arc1 = [(heading_start[0] - heading_height/2,
                     heading_start[1]),
                    (heading_start[0] + heading_height/2,
                     heading_end[1])]
            arc2 = [(heading_end[0] - heading_height/2,
                     heading_start[1]),
                    (heading_end[0] + heading_height/2,
                     heading_end[1])]

            # Paste the two semicircles and rectangle.     
            display_canvas.rectangle([heading_start, heading_end], fill=icon_color)
            display_canvas.pieslice(arc1, 90, 270, fill=icon_color)
            display_canvas.pieslice(arc2, 270, 90, fill=icon_color)

            # Paste the text on top of the completed heading shapes.
            display_canvas.text(heading_start, key, font=font60, fill=font_color)

            # Calculate where the information is displayed under the
            # heading.
            value_start = (display_middle-font60.getsize(value)[0]/2,
                          x_down + heading_height + heading_gap)

            # Paste the information underneath the heading.
            display_canvas.text(value_start, value, font=font60, fill=icon_color)


        # The following section deals with the closest color name and
        # associated flavor text.

        # Split the name into lines so that it doesn't overflow.
        name_lines = textwrap.wrap(msg["name"], width=15,
                             break_long_words=False,
                             break_on_hyphens=False)

        # Reconstitute the text with newlines such that it doesn't overflow.
        name = '\n'.join(name_lines)

        # Calculate where the name and flavor text should be displayed based
        # on the size of the name.
        name_start = 2000 - len(name_lines)*100
        prename_start = name_start - 100
        
        # Find where the flavor text should be positioned taking into
        # account the font used.
        prename_start = findStart((display_middle, prename_start),
                                 msg["prename"], font50)
        
        # Find the length of the largest line in the name.
        largest_line_length = max(name_lines, key=len)

        # Find where the name should be positioned taking into account
        # the font used.
        name_start = findStart((display_middle, name_start),
                              largest_line_length, font70)

        # Paste the flavor text onto the canvas in the correct position.
        display_canvas.text(prename_start, msg["prename"],
                            font=font50, fill=icon_color)

        # Paste the name onto the canvas in the correct position.
        display_canvas.multiline_text(name_start, name, font=font70,
                              fill=icon_color, spacing=8, align="center")

        # Paste the working_display onto the original image with the color.
        base_image.paste(working_display, (display_start, 0))

    # Return the finished image.
    return base_image

def retrieve_theme():
    '''
        Retrieves the current theme from the themes subdirectory
        and returns a ColorTheme object with the colors contained
        within that theme.

        Returns:
            A ColorTheme object representing the current theme.
    '''
    # Read what the current theme is.
    with open(sys.path[0] + "/themes/current.txt", "r") as f:
        theme_name = f.readline()
        
    # Get the colors associated with the theme from the themes.json
    # file imported at the start of this script.
    theme = themes[theme_name]

    # Create an empty ColorTheme object with the correct name.
    result = js.ColorTheme(theme_name)

    # Import the colors associated with the theme into the ColorTheme
    # object and return it.
    result.importTheme(theme)
    return result
    
    
def post():
    '''
        Makes a post through the Facebook Graph API which consists of
        a picture of a color as well as information about that color.
        Then, adds a comment to that post with the plain version of
        that image and a transcripted version of the information.

        The color chosen is at random, but is selected with the current
        theme in mind.
    '''
    # Retrieve the current theme and generate a random color from that
    # theme.
    current_theme = retrieve_theme()
    colors = [current_theme.getRandom() for i in range(2)]

    # Create two images - one is a plain image of the color and the other
    # also has additional information appended to the right side.

    color_template = genTemplateColor(colors)

    color_plain = genPlainColor(colors)

    # Create text containing the theme name to be posted with the
    # image containing the information display.
    theme = "Theme: %s" % current_theme.getName()

    # Generate a plaintext message containing the information about the
    # color.
    r, g, b = colors[0]
    msg1 = genMessage(r, g, b)
    msg1 = '\n'.join([
        "RGB: (%s, %s, %s)" % msg1["RGB"],
        "CMYK: (%.2f, %.2f, %.2f, %.2f)" % msg1["CMYK"],
        "HSV: %.1f°, %.1f%%, %.1f%%" % msg1["HSV"],
        "HEX: %s" % msg1["HEX"],
        "WAVELENGTH: %s" % msg1["WAVE"],
        "%s %s" % (msg1["prename"], msg1["name"])
        ])
    r, g, b = colors[1]
    msg2 = genMessage(r, g, b)
    msg2 = '\n'.join([
        "RGB: (%s, %s, %s)" % msg2["RGB"],
        "CMYK: (%.2f, %.2f, %.2f, %.2f)" % msg2["CMYK"],
        "HSV: %.1f°, %.1f%%, %.1f%%" % msg2["HSV"],
        "HEX: %s" % msg2["HEX"],
        "WAVELENGTH: %s" % msg2["WAVE"],
        "%s %s" % (msg2["prename"], msg2["name"])
        ])

    msg = "Color 1:\n%s \n\nColor 2:\n%s" % (msg1, msg2)

    # Print the message as confirmation that the script has worked.
    print(msg)

    # Save the image and then post it to the Facebook Graph API.
    color_template.save(sys.path[0] + '/image.png', 'PNG')
    post_id = graph.put_photo(image=open(sys.path[0] + '/image.png', 'rb'),
                             message=theme)['post_id']

    # Save the post id to the post ids folder for later use in the
    # top likers / statistics portion of the page.
    with open(sys.path[0] + '/postids/postids.txt', 'a') as f:
        f.write(str(post_id) + '\n')

    # Add a comment with the plain color and plaintext information to
    # the post that was just made.
    color_plain.save(sys.path[0] + '/image.png', 'PNG')
    graph.put_photo(image=open(sys.path[0] + '/image.png', 'rb'),
                    message = msg, album_path=str(post_id) + '/comments')


def custom():
    '''
        Makes a random color but does not post it to the facebook page.

        The color chosen is at random, but is selected with the current
        theme in mind.
    '''
    # Retrieve the current theme and generate a random color from that
    # theme.
    current_theme = retrieve_theme()

    colors = [[29, 68, 108], [241, 241, 241]]

    color_template = genTemplateColor(colors)

    # Create text containing the theme name to be posted with the
    # image containing the information display.
    theme = "Theme: %s" % current_theme.getName()

    # Generate a plaintext message containing the information about the
    # color.
    r, g, b = colors[0]
    msg1 = genMessage(r, g, b)
    msg1 = '\n'.join([
        "RGB: (%s, %s, %s)" % msg1["RGB"],
        "CMYK: (%.2f, %.2f, %.2f, %.2f)" % msg1["CMYK"],
        "HSV: %.1f°, %.1f%%, %.1f%%" % msg1["HSV"],
        "HEX: %s" % msg1["HEX"],
        "WAVELENGTH: %s" % msg1["WAVE"],
        "%s %s" % (msg1["prename"], msg1["name"])
        ])
    r, g, b = colors[1]
    msg2 = genMessage(r, g, b)
    msg2 = '\n'.join([
        "RGB: (%s, %s, %s)" % msg2["RGB"],
        "CMYK: (%.2f, %.2f, %.2f, %.2f)" % msg2["CMYK"],
        "HSV: %.1f°, %.1f%%, %.1f%%" % msg2["HSV"],
        "HEX: %s" % msg2["HEX"],
        "WAVELENGTH: %s" % msg2["WAVE"],
        "%s %s" % (msg2["prename"], msg2["name"])
        ])

    msg = "Color 1:\n%s \n\nColor 2:\n%s" % (msg1, msg2)

    # Print the message as confirmation that the script has worked.
    print(msg)

    # Save the image and then post it to the Facebook Graph API.
    color_template.save(sys.path[0] + '/image.png', 'PNG')
