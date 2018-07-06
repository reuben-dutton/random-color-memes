import sys
import json
import random

'''
    This file selects a random theme from the available ones and
    sets it to be the current theme. This does not take into account
    a theme vote.
'''

# Load the themes.
themes = json.loads(open(sys.path[0] + '/../json/themes.json').read())

# Select a random theme. If the random theme is 'None', continue
# selecting a random theme until it isn't.
theme = random.choice(list(themes.keys()))
while theme == "None":
    theme = random.choice(list(themes.keys()))

# Save the randomly selected theme as the current theme.
with open(sys.path[0] + "/current.txt", "w") as currentfile:
    currentfile.write(theme)
