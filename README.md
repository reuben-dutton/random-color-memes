# Random Color Memes

This script generates an image of a random color as well as information about that color and posts it to the [Random Color Memes](https://www.facebook.com/randomcolormemes/) Facebook page.

![Example Color](https://i.imgur.com/pBjk2rE.png?raw=true)

## Short Explanation
The script generates 3 random integers between 0 and 255 - this corresponds to a color in the [RGB](https://en.wikipedia.org/wiki/RGB_color_space) color space. It then transforms these values to their equivalent coordinates in the [CMYK](https://en.wikipedia.org/wiki/CMYK_color_model) and [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV) color spaces. Additionally, it produces a hexadecimal representation of the RGB value. 
If possible, it then generates an [approximate wavelength](https://en.wikipedia.org/wiki/Visible_spectrum) value on the visible spectrum. For some colors this isn't possible as they are a combination of multiple wavelengths, so the image instead displays 'N/A'. 
Lastly, the script determines which color from [this list](https://en.wikipedia.org/wiki/List_of_colors) is visually closest to the random color and displays the name and a bit of flavor text alongside it (this text indicates how close the color is).

The page also has a few automated functions:

 - **Top Reacters List**
 
 The scripts above keep track of how many reactions each person who likes the page makes within specific timeframes. At certain points in the month, a post is made to the page with the names, total reactions and rank of the top 50 reacters (for the last 15 days if it's a bimonthly list, and the last month if it's a monthly list).
 
 - **Theme Days**
 
 The script also has the capability to select a random color within a select subset of colours. For instance, an 'Ocean' theme may only allow blues and aqua greens to be selected as the random color. For each theme day, a theme is selected either through a community vote (where the day before the theme is used users vote from a random selection of 6 themes for which one they want) or is selected randomly. In either case, the theme is used for 24 hours (a day), during which the script only selects colours from within that theme.
 
## Schedule

The page follows the following schedule as of 8/07/2018. Note that the schedule is dependent on the month rather than the week. (Color votes have not been implemented, but they will likely be added in those positions on the calendar)

![Schedule](https://i.imgur.com/jyXM3fq.jpg?raw=true)

## Currently Implemented
 - **Color Spaces**
     - RGB
     - CMYK
     - HSV
     - Hexadecimal
     - Approximate Wavelength
     - Approximate color name + flavor text
     
 - **Facebook Page Events**
     - Top likers twice every month
     - Theme days (using colors with a particular theme, e.g. forests, oceans, etc.)
     
     
## To Be Implemented
 - **Color Spaces**
     - HSL (?)
     - [Relative Brightness](https://en.wikipedia.org/wiki/Brightness) (?)
     - [LMS color space](https://en.wikipedia.org/wiki/LMS_color_space) (?)
     
 - **Facebook Page Events**
     - Vote on color names (using reactions to keep track of votes)
     
