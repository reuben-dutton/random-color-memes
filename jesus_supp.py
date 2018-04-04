import random, math

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
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        while not self.contains((r, g, b)):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
        return (r, g, b)
