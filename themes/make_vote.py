import facebook, requests
import math, random
import json
import sys

env = json.loads(open(sys.path[0] + '/../env.json').read())
page_id = env['page_id']
acstoke = env['page_token']
graph = facebook.GraphAPI(access_token=acstoke)

themes = json.loads(open(sys.path[0] + '/../json/themes.json').read())

chosen_themes = random.sample(list(themes.keys()), 6)

reactions = {
    "LIKE": chosen_themes[0],
    "LOVE": chosen_themes[1],
    "HAHA": chosen_themes[2],
    "WOW": chosen_themes[3],
    "SAD": chosen_themes[4],
    "ANGRY": chosen_themes[5]
    }

with open(sys.path[0] + "/votereactions.json", "w") as votefile:
    json.dump(reactions, votefile)

msg = "THEME VOTE" \
      + "\n" \
      + "\n" \
      + "\n" \
      + "REACT to the post to vote for a theme" \
      + "\n" \
      + "The theme of the week will be the" \
      + " selected from the two highest voted themes" \
      + "\n" \
      + u"\U0001F44D" + " - " + chosen_themes[0] + "\n" \
      + u"\U0001F493" + " - " + chosen_themes[1] + "\n" \
      + u"\U0001F602" + " - " + chosen_themes[2] + "\n" \
      + u"\U0001F62E" + " - " + chosen_themes[3] + "\n" \
      + u"\U0001F622" + " - " + chosen_themes[4] + "\n" \
      + u"\U0001F620" + " - " + chosen_themes[5] + "\n" \
      + "\n" \
      + "This vote will close 24 hours after this" \
      + " post is made. Feel free to comment some" \
      + " possible themes and colors for the future" \
      + " below! I'll add the best ones in <3"
      
postid = graph.put_object(parent_object="me", connection_name="feed", message=msg)

with open(sys.path[0] + "/votepostid.txt", "w") as vpidfile:
    vpidfile.write(postid["id"])
