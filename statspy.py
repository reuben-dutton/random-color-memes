import facebook, requests


## requires page id and access token to access that page
page_id = "1250450778363053"
acstoke = "EAAaKi61MD2cBAA8NTsXSPFaKwStELjL8JSg0jf11xPY1dhzAwy33u5ui4aoP6Olvv7cs12QTTdK5Uzle3rRAzDY6oAxrtHGq0KVqFNaSBkmkTr6UsfzkOi7b6bLkQyc6ZBpBioK3z0z0ZBZC2NrcoFhiDLfEsj03rEfIJDXvwZDZD"   
## for facebook graph API
graph = facebook.GraphAPI(access_token=acstoke)

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
    for i in range(100):
        score = ranklikes[i]
        try:
            userdict = graph.get_object(rankids[i], fields="name")
        except IndexError:
            print('No more in the list')
            return
        username = userdict['name']
        try:
            if score == tiedscore:
                print('Tied ' + str(scorenumber) + ' - ' + str(score) + ' - ' + str(username))
            elif score < tiedscore:
                scorenumber = i+1
                if ranklikes[scorenumber] == ranklikes[scorenumber-1] and scorenumber < 100:
                    print('Tied ' + str(scorenumber) + ' - ' + str(score) + ' - ' + str(username))
                else:
                    print(str(scorenumber) + ' - ' + str(score) + ' - ' + str(username))
                tiedscore = score
        except IndexError:
            pass
    
    



    
