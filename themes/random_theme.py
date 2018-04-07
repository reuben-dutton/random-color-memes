import sys
import json
import random

themes = json.loads(open(sys.path[0] + '/../json/themes.json').read())
theme = random.choice(list(themes.keys()))
with open(sys.path[0] + "/current.txt", "w") as currentfile:
    currentfile.write(theme)
