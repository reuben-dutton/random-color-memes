import random, math
from numpy.random import choice

class ColorBubble():
    
    def __init__(self, origin, radius):
        self._o = tuple(origin)
        self._r = radius

    def __hash__(self):
        return hash((self._o, self._r))

    def __eq__(self, other):
        return other and self._o == other._o and self._r == other._r

    def contains(self, point):
        xdiff = self._o[0] - point[0]
        ydiff = self._o[1] - point[1]
        zdiff = self._o[2] - point[2]
        if not (0 <= point[0] <= 255):
            return False
        elif not (0 <= point[1] <= 255):
            return False
        elif not (0 <= point[2] <= 255):
            return False
        else:
            return (xdiff**2 + ydiff**2 + zdiff**2 <= self._r**2)

    def getRandom(self):
        r = random.randint(self._o[0] - self._r, self._o[0] + self._r)
        g = random.randint(self._o[1] - self._r, self._o[1] + self._r)
        b = random.randint(self._o[2] - self._r, self._o[2] + self._r)
        while not self.contains((r, g, b)):
            r = random.randint(self._o[0] - self._r, self._o[0] + self._r)
            g = random.randint(self._o[1] - self._r, self._o[1] + self._r)
            b = random.randint(self._o[2] - self._r, self._o[2] + self._r)
        return (r, g, b)

class ColorTheme():

    def __init__(self, name):
        self._name = name
        self._cbs = set()

    def addBubble(self, colorbubble):
        self._cbs.add(colorbubble)

    def getName(self):
        return self._name

    def importTheme(self, bubbleList):
        for bubble in bubbleList:
            cb = ColorBubble(bubble[0], bubble[1])
            self.addBubble(cb)

    def contains(self, point):
        returnvalue = False
        for bubble in self._cbs:
            returnvalue = (returnvalue or bubble.contains(point))
        return returnvalue
        
    def getRandom(self):
        weights = [bubble._r for bubble in list(self._cbs)]
        total = sum(weights)
        weights = [w/total for w in weights]
        bubble = choice(list(self._cbs), p=weights)
        return bubble.getRandom()
