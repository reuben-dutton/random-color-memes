import facebook
import requests
import random
import json
import sys

'''
    This file posts a theme vote to the page. It also saves the post id
    of the vote as well as a json file keeping track of what reactions
    are associated with which themes.
'''

# Import the details for the page and link to the Facebook API.
env = json.loads(open(sys.path[0] + '/../env.json').read())
page_id = env['page_id']
acstoke = env['page_token']
graph = facebook.GraphAPI(access_token=acstoke)

# Loads the possible themes from the json directory.
themes = json.loads(open(sys.path[0] + '/../json/themes.json').read())

# Selects 6 theme names at random from the themes list and saves the
# results to a list.
chosen_themes = random.sample(list(themes.keys()), 5)

# Assigns each theme a reaction.
reactions = {
    "LOVE": chosen_themes[0],
    "HAHA": chosen_themes[1],
    "WOW": chosen_themes[2],
    "SAD": chosen_themes[3],
    "ANGRY": chosen_themes[4]}

# Saves the reaction assignment to a json file for later reference.
with open(sys.path[0] + "/votereactions.json", "w") as votefile:
    json.dump(reactions, votefile)

# Creates a message for the theme vote post.
msg = "THEME VOTE" \
      + "\n" \
      + "\n" \
      + "\n" \
      + "REACT to the post to vote for a theme" \
      + "\n" \
      + "The theme of the week will be the" \
      + " selected highest voted theme." \
      + "\n" \
      + u"\U0001F493" + " - " + chosen_themes[0] + "\n" \
      + u"\U0001F602" + " - " + chosen_themes[1] + "\n" \
      + u"\U0001F62E" + " - " + chosen_themes[2] + "\n" \
      + u"\U0001F622" + " - " + chosen_themes[3] + "\n" \
      + u"\U0001F620" + " - " + chosen_themes[4] + "\n" \
      + "\n" \
      + "This vote will close 24 hours after this" \
      + " post is made. Feel free to comment some" \
      + " possible themes and colors for the future" \
      + " below! I'll add the best ones in <3"

# Makes a post to the page with the above message.
postid = graph.put_object(parent_object="me", connection_name="feed",
                          message=msg)

# Saves the post id to the 'votepostid.txt' file for later use.
with open(sys.path[0] + "/votepostid.txt", "w") as vpidfile:
    vpidfile.write(postid["id"])
