import facebook, requests
import sys
import json
import stats

'''
    This file does the bimonthly top reacters post. It appends
    the current post ids to the (empty) monthly post ids and
    tabulates the rankings, then deletes the current post ids.
'''

# Import the details for the page and link to the Facebook API.
env = json.loads(open(sys.path[0] + '/../env.json').read())
page_id = env['page_id']
_access_token = env['page_token']
graph = facebook.GraphAPI(access_token=_access_token)

# Perform the bimonthly top reacters list.
stats.writemonthly()
graph.put_object(parent_object='me', connection_name='feed',
                 message=stats.rs(False))
stats.deletecurrent()

