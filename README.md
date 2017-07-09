# Random Color Memes

![Example Color](fancy.png?raw=true)

This script generates a random color every hour along with bits of relevant information (demonstrated in the image above) and posts the image to the [Random Color Memes](https://www.facebook.com/randomcolormemes/) Facebook page.

## Short Explanation
The script generates 3 random integers in the range (0, 255) inclusive, which then corresponds to a value in the [RGB](https://en.wikipedia.org/wiki/RGB_color_space) color space. It then converts these values to the respective values in the [CMYK](https://en.wikipedia.org/wiki/CMYK_color_model) and [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV) color spaces. Additionally, it produces a hexadecimal representation of the RGB value. 
If possible, it then generates an [approximate wavelength](https://en.wikipedia.org/wiki/Visible_spectrum) value on the visible spectrum. For some colors this isn't possible as they are a combination of multiple wavelengths, so the image instead displays 'N/A'. 
Lastly, the color is given a name depending on how close it is to that named color [(according to Wikipedia)](https://en.wikipedia.org/wiki/List_of_colors).

The statistics script is used to get the likes and reactions on every post on the page, and then collates and organises these reactions based on user and reaction. For instance, if the script is used to look for the amount of likes and it returns:
```
Tom Jones - 15
Abigail Thompson - 7
Jenny Pilkington - 2
```
This means that Tom has liked 15 posts in total, Abigail has liked 7 in total, and Jenny has liked 2 posts in total. This information is then used to manually produce a 'top likers' post on the first of each month.

## Currently Implemented
 - **Color Spaces**
     - RGB
     - CMYK
     - HSV
     - Hexadecimal
     - Approximate Wavelength
     - Color Name
     
 - **Facebook Page Events**
     - Top likers every month
     
     
## To Be Implemented
 - **Color Spaces**
     - HSL
     - [Relative Brightness](https://en.wikipedia.org/wiki/Brightness)
     - [LMS color space](https://en.wikipedia.org/wiki/LMS_color_space)
     
 - **Facebook Page Events**
     - Themed weeks (using colors with a particular theme, e.g. forests, oceans, etc.)
     - Vote on color names (using reactions to keep track of votes)
     - Vote on events (using reactions)
     
