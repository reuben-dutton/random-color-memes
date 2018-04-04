import facebook, requests
import json
import sys

env = json.loads(open(sys.path[0] + '/../env.json').read())
page_id = env['page_id']
acstoke = env['page_token']
graph = facebook.GraphAPI(access_token=acstoke)


with open(sys.path[0] + "/votepostid.txt", "r") as vpidfile:
    vpid = vpidfile.readline()

vr = json.loads(open(sys.path[0] + '/votereactions.json').read())

data = graph.get_object(id=vpid, fields="reactions")
results = dict()

for react in data['reactions']['data']:
    react_type = react['type']
    theme = vr[react_type]
    results[theme] = results.get(theme, 0) + 1

items = list(results.values())
keys = list(results.keys())
theme = keys[items.index(max(items))]

with open(sys.path[0] + "/current.txt", "w") as currentfile:
    currentfile.write(theme)
