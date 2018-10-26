import facebook
import requests
import json
import sys

'''
    This file retrieves a theme vote from the page, determines the
    winner of the vote and then saves that winning theme into the
    'current.txt' text file.
'''

# Import the details for the page and link to the Facebook API.
env = json.loads(open(sys.path[0] + '/../env.json').read())
page_id = env['page_id']
_access_token = env['page_token']
graph = facebook.GraphAPI(access_token=_access_token)

# Retrieve the post id for the theme vote from the 'votepostid.txt'
# text file.
with open(sys.path[0] + "/votepostid.txt", "r") as vpidfile:
    vpid = vpidfile.readline()

# Load the dictionary which says which themes are associated with
# what reactions in the vote.
vr = json.loads(open(sys.path[0] + '/votereactions.json').read())

# Retrieve the reactions on the theme vote post.
data = graph.get_object(id=vpid, fields="reactions")
results = dict()

# Tabulate the reactions.
for react in data['reactions']['data']:
    react_type = react['type']
    theme = vr[react_type]
    results[theme] = results.get(theme, 0) + 1

# Determine which theme had the most votes by reactions.
items = list(results.values())
keys = list(results.keys())
theme = keys[items.index(max(items))]

# Set the current theme to the winning theme.
with open(sys.path[0] + "/current.txt", "w") as currentfile:
    currentfile.write(theme)
