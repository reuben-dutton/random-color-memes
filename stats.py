import facebook, requests


env = json.loads(open('env.json').read())

page_id = env['page_id']
at = env['page_token']
graph = facebook.GraphAPI(access_token=at)

def retrieve_stats(reaction):
    f = open('objectids.txt', 'r')
    likes = []
    for line in f:
        objID = line.replace('\n', '')
        likes.append((graph.get_object(objID + '/reactions', limit=100))['data'])
    f.close()

    ranking = {}
    for post in likes:
        for minidict in post:
            if minidict['type'] in reaction:
                userid = minidict['id']
                ranking[userid] = ranking.get(userid, 0) + 1

    ranklikes = sorted(ranking.values(), reverse=True)
    rankids = sorted(ranking, key=ranking.__getitem__, reverse=True)


    tiedscore = ranklikes[0]+1
    scorenumber = 1
    end_string = ''
    for i in range(100):
        score = ranklikes[i]
        try:
            userdict = graph.get_object(rankids[i], fields="name")
        except IndexError:
            return
        username = userdict['name']
        try:
            if score == tiedscore:
                end_string.append('Tied ' + str(scorenumber) + ' - ' + str(score) + ' - ' + str(username))
                end_string.append('\n')
            elif score < tiedscore:
                scorenumber = i+1
                if ranklikes[scorenumber] == ranklikes[scorenumber-1] and scorenumber < 100:
                    end_string.append('Tied ' + str(scorenumber) + ' - ' + str(score) + ' - ' + str(username))
                    end_string.append('\n')
                else:
                    end_string.append(str(scorenumber) + ' - ' + str(score) + ' - ' + str(username))
                    end_string.append('\n')
                tiedscore = score
        except IndexError:
            pass
    
    



    
