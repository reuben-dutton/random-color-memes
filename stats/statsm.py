import facebook, requests
import sys
import json
import stats

'''
    This file does the monthly top reacters post. It appends
    the current post ids to the monthly post ids, appends the
    newly appended monthly post ids to the all time post ids,
    tabulates the rankings, then deletes the current post ids
    and the monthly post ids.
'''

# Import the details for the page and link to the Facebook API.
env = json.loads(open(sys.path[0] + '/../env.json').read())
page_id = env['page_id']
at = env['page_token']
graph = facebook.GraphAPI(access_token=at)

# Perform the monthly top reacters list.
stats.writemonthly()
stats.writealltime()
graph.put_object(parent_object='me', connection_name='feed',
                 message=stats.rs(True))
stats.deletecurrent()
stats.deletemonthly()

