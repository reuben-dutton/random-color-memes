import facebook, requests
import sys
import json
import stats as s


env = json.loads(open(sys.path[0] + '/../env.json').read())

page_id = env['page_id']
at = env['page_token']
graph = facebook.GraphAPI(access_token=at)

s.writemonthly()
s.writealltime()
graph.put_object(parent_object='me', connection_name='feed', message=s.rs(True))
s.deletecurrent()
s.deletemonthly()

