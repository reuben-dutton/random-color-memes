import facebook, requests
import sys
import json


env = json.loads(open(sys.path[0] + '/../env.json').read())

page_id = env['page_id']
at = env['page_token']
graph = facebook.GraphAPI(access_token=at)

def rs(monthly, reaction=['LIKE', 'LOVE', 'WOW', 'SAD', 'ANGRY', 'HAHA']):
    if monthly:
        f = open(sys.path[0] + '/postidsmonthly.txt', 'r')
    else:
        f = open(sys.path[0] + '/postids.txt', 'r')
    likes = []
    ranking = {}
    for line in f:
        objID = line.replace('\n', '')
        data = graph.get_object(objID + '/reactions', limit=100)['data']
        
        for minidict in data:
            if minidict['type'] in reaction:
                userid = minidict['id']
                ranking[userid] = ranking.get(userid, 0) + 1

    f.close()

    ranklikes = sorted(ranking.values(), reverse=True)
    rankids = sorted(ranking, key=ranking.__getitem__, reverse=True)

    tiedscore = ranklikes[0]+1
    scorenumber = 1
    
    end_string = 'TOP REACTS (' + monthly + ')'
    for i in range(50):
        try:
            score = ranklikes[i]
            userdict = graph.get_object(rankids[i], fields="name")
        except IndexError:
            break
        username = userdict['name']
        try:
            if score == tiedscore:
                end_string = '\n'.join([end_string, 'Tied {} - {} - {}'.format(scorenumber, score, username)])
            elif score < tiedscore:
                scorenumber = i+1
                if ranklikes[scorenumber] == ranklikes[scorenumber-1] and scorenumber < 100:
                    end_string = '\n'.join([end_string, 'Tied {} - {} - {}'.format(scorenumber, score, username)])
                else:
                    end_string = '\n'.join([end_string, '{} - {} - {}'.format(scorenumber, score, username)])
                tiedscore = score
        except IndexError:
            pass
    return end_string

def writealltime():
    f2 = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'r')
    f3 = open(sys.path[0] + '/../postids/postidsalltime.txt', 'a')
    for line in f2:
        f3.write(line)
    f2.close()
    f3.close()

def writemonthly()
    f1 = open(sys.path[0] + '/../postids/postids.txt', 'r')
    f2 = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'a')
    for line in f1:
        f2.write(line)
    f1.close()
    f2.close()

def deletecurrent():
    f = open(sys.path[0] + '/../postids/postids.txt', 'w')
    f.write('')
    f.close()

def deletemonthly():
    f = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'w')
    f.write('')
    f.close()


arg = sys.argv[1]
if arg == "Monthly":
    writemonthly()
    writealltime()
    graph.put_object(parent_object='me', connection_name='feed', message=rs(True))
    deletecurrent()
    deletemonthly()
elif arg == "Bimonthly":
    writemonthly()
    graph.put_object(parent_object='me', connection_name='feed', message=rs(False))
    deletecurrent()

