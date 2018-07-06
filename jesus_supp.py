import random, math
from numpy.random import choice

'''
    This file contains some support code regarding the themes the
    page does every so often. It only contains classes which are
    used to represent themes and some helper methods which are used
    to get random colors from a theme, get the name of a theme, etc.
'''

class ColorBubble():
    '''
        An abstract class representing a closed ball within the RGB
        color space.

        Attributes:
            o (tuple(float, float, float)): The centre of the ball.
            r (float): The radius of the ball.
    '''
    
    def __init__(self, origin, radius):
        '''
            The initialisation method for the class

            Args:
                origin (list): The desired centre of the
                                      ColorBubble.
                radius (float): The desired radius of the ColorBubble.
        '''
        self._o = tuple(origin)
        self._r = radius

    def __hash__(self):
        return hash((self._o, self._r))

    def __eq__(self, other):
        return other and self._o == other._o and self._r == other._r

    def contains(self, point):
        '''
            Checks if the ColorBubble contains a given point.

            Args:
                point (tuple(float, float, float)): A point in 3D space.

            Returns:
                True if the point is contained within the bubble,
                False otherwise.
        '''
        # Find the distance between the point and the origin.
        xdiff = self._o[0] - point[0]
        ydiff = self._o[1] - point[1]
        zdiff = self._o[2] - point[2]

        # If the point is outside the RGB color space, return False.
        # If the distance between the origin and the point is
        # greater than the radius, return False. Else, return True.
        if not (0 <= point[0] <= 255):
            return False
        elif not (0 <= point[1] <= 255):
            return False
        elif not (0 <= point[2] <= 255):
            return False
        else:
            return (xdiff**2 + ydiff**2 + zdiff**2 <= self._r**2)

    def getRandom(self):
        '''
            Get a random point from within the ColorBubble.

            Returns:
                A tuple representing a random color within the
                RGB space contained within the ColorBubble.
        '''
        # Select random r, g and b values within the cube of 2r length
        # centred around the origin.
        r = random.randint(self._o[0] - self._r, self._o[0] + self._r)
        g = random.randint(self._o[1] - self._r, self._o[1] + self._r)
        b = random.randint(self._o[2] - self._r, self._o[2] + self._r)

        # Continue retrieving points in the above fashion until one
        # is also within the ColorBubble. Then, return that color.
        while not self.contains((r, g, b)):
            r = random.randint(self._o[0] - self._r,
                               self._o[0] + self._r)
            g = random.randint(self._o[1] - self._r,
                               self._o[1] + self._r)
            b = random.randint(self._o[2] - self._r,
                               self._o[2] + self._r)
            
        return (r, g, b)

class ColorTheme():
    '''
        An abstract class representing a theme of colors. That is, it
        is a series of ColorBubble objects which represent a space of
        colors associated with that theme.

        Attributes:
            name (str): The name of the color theme.
            cbs (set(ColorBubble)): A set of ColorBubbles associated
                                     with the theme.
    '''
    def __init__(self, name):
        '''
            The initialisation method for the class.

            Args:
                name (string): The name for the ColorTheme.
        '''
        self._name = name
        # Creates an empty set of ColorBubble objects.
        self._cbs = set()

    def addBubble(self, colorbubble):
        '''
            Adds a ColorBubble to the theme.

            Args:
                colorbubble (ColorBubble): A ColorBubble object.
        '''
        self._cbs.add(colorbubble)

    def getName(self):
        ''' Return the name of the theme. '''
        return self._name

    def importTheme(self, bubble_list):
        '''
            Import a list of tuples containing origin and radii into
            the theme by converting them into ColorBubble objects.

            Args:
                bubble_list (list(tuple(float, float, float))):
                        A list containing origin and radii values
                        for the creation of ColorBubble objects.
        '''
        for bubble in bubble_list:
            cb = ColorBubble(bubble[0], bubble[1])
            self.addBubble(cb)

    def contains(self, point):
        '''
            Check if a given point is contained within the theme.

            Args:
                point (tuple(float, float, float)): A point within the
                                                    RGB color space.
                                                    
            Returns:
                True if the point is within the theme, False otherwise.
        '''
        # Set the return value to be initially False.
        returnvalue = False

        # If the point is contained within a particular bubble, then
        # set the return value to True.
        for bubble in self._cbs:
            returnvalue = (returnvalue or bubble.contains(point))

        # Return the return value.
        return returnvalue
        
    def getRandom(self):
        '''
            Get a random point from within the theme. Each bubble
            within the theme is weighted based on the radius of
            the bubble.

            Returns:
                A tuple representing a random point within the theme.
        '''
        # Set the weight for each bubble to be in proportion to
        # the size of each bubble (using radius).
        weights = [bubble._r for bubble in list(self._cbs)]
        total = sum(weights)
        weights = [w/total for w in weights]

        # Retrieve a random ColorBubble from within the theme using
        # the weights calculated above.
        bubble = choice(list(self._cbs), p=weights)

        # Return a random color from within the selected ColorBubble.
        return bubble.getRandom()
