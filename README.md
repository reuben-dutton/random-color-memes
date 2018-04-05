# Random Color Memes

![Example Color](fancy.png?raw=true)

This script generates a random color every hour along with bits of relevant information (demonstrated in the image above) and posts the image to the [Random Color Memes](https://www.facebook.com/randomcolormemes/) Facebook page.

## Short Explanation
The script generates 3 random integers in the range (0, 255) inclusive, which then corresponds to a value in the [RGB](https://en.wikipedia.org/wiki/RGB_color_space) color space. It then converts these values to the respective values in the [CMYK](https://en.wikipedia.org/wiki/CMYK_color_model) and [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV) color spaces. Additionally, it produces a hexadecimal representation of the RGB value. 
If possible, it then generates an [approximate wavelength](https://en.wikipedia.org/wiki/Visible_spectrum) value on the visible spectrum. For some colors this isn't possible as they are a combination of multiple wavelengths, so the image instead displays 'N/A'. 
Lastly, the color is given a name depending on how close it is to that named color [(according to Wikipedia)](https://en.wikipedia.org/wiki/List_of_colors).

The page also has a few automated functions - theme weeks and top reacters lists.

The top reacters list is posted twice every month; it is posted on the 15th of each month (which is for all posts between then and the 1st of the month) as well as the 1st of each month (which is for all posts between the 1st of that month and the 1st of the last month).

The theme weeks are done between the 8th and 14th of every month. On the 8th, users on the page are are asked to vote for a particular theme (one of six) by reacting to a post made on the page. A specific reaction is assigned to each possible theme, and reacting to the post in a certain way 'votes' for that theme. The next day, the 'votes' are tallied up and the new theme is set. From the 9th until the 14th, the page only posts colors associated with that particular theme. After the 14th, the page resets back to normal. 

## Currently Implemented
 - **Color Spaces**
     - RGB
     - CMYK
     - HSV
     - Hexadecimal
     - Approximate Wavelength
     - Color Name
     
 - **Facebook Page Events**
     - Top likers twice every month
     - Themed weeks (using colors with a particular theme, e.g. forests, oceans, etc.)
     
     
## To Be Implemented
 - **Color Spaces**
     - HSL
     - [Relative Brightness](https://en.wikipedia.org/wiki/Brightness)
     - [LMS color space](https://en.wikipedia.org/wiki/LMS_color_space)
     
 - **Facebook Page Events**
     - Vote on color names (using reactions to keep track of votes)
     - Vote on events (using reactions)
     
