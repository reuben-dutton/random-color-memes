import sys
import json
import facebook, requests

'''
    This file contains the statistics portion of the project. It contains
    support code essential for statsb.py and statsm.py, which is used to
    retrieve the reactions on a series of posts given their post ids.
    Then, the information is tabulated and grouped by the person
    reacting in order to create a ranking determining who reacted to the
    most posts within a certain timeframe.

    Post ids are separated into three files:
        postids.txt - containing the most recent post ids
        postidsmonthly.txt - containing post ids from the current month
        postidsalltime.txt - containng all post ids

    Stats are done like so:

    Post ids are only added to postids.txt when the post is made. They
    are not added to any other file when the post is initially made.

    Halfway through the month, stats are compiled based on the post ids
    within postids.txt. Then these post ids are emptied into
    postidsmonthly.txt.

    At the start of each month, stats are compiled based on the post ids
    within postidsmonthly.txt. These post ids are then emptied into
    postidsalltime.txt.
    
'''

# Import the details for the page and link to the Facebook API.
env = json.loads(open(sys.path[0] + '/../env.json').read())
page_id = env['page_id']
_access_token = env['page_token']
graph = facebook.GraphAPI(access_token=_access_token)


def rs(monthly, reaction=['LIKE', 'LOVE', 'WOW', 'SAD', 'ANGRY', 'HAHA']):
    '''
        A function to retrieve the stats depending on what time it is.

        Args:
            monthly (Boolean): Whether the states are monthly (as
                               opposed to bimonthly)

        Returns:
            A formatted string containing the top 50 reacters in the
            designated time period.
    '''

    # Determine which post ids to use (monthly or bimonthly).
    if monthly:
        f = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'r')
        end_string = 'TOP REACTS (Monthly)'
    else:
        f = open(sys.path[0] + '/../postids/postids.txt', 'r')
        end_string = 'TOP REACTS (Bimonthly)'
    
    likes = []
    ranking = {}

    # Retrieve the reactions on each post and compile them based on
    # the user id doing the reacting.
    for line in f:
        objID = line.replace('\n', '')
        data = graph.get_object(objID + '/reactions', limit=100)['data']
        
        for minidict in data:
            try:
                if minidict['type'] in reaction:
                    userid = minidict['id']
                    ranking[userid] = ranking.get(userid, 0) + 1
            except:
                pass

    f.close()

    # Get a list containing the total reactions for each userid in
    # descending order. Also compile a list of userids which are
    # also align to the previous list (i.e. entry 1 corresponds to
    # entry 1 for both lists)
    rank_likes = sorted(ranking.values(), reverse=True)
    rank_ids = sorted(ranking, key=ranking.__getitem__, reverse=True)

    tied_score = rank_likes[0]+1
    score_number = 1

    # Append to the return string for every user in the top 50.
    # If the score is equal to the current tiedscore, then also add
    # 'Tied' to the line and keep the current rank number the same.
    for i in range(50):
        try:
            score = rank_likes[i]
            user_dict = graph.get_object(rank_ids[i], fields="name")
        except IndexError:
            break
        user_name = user_dict['name']
        try:
            if score == tied_score:
                end_string = '\n'.join([end_string,
                                        'Tied {} - {} - {}'.format(score_number, score, user_name)])
            elif score < tied_score:
                score_number = i+1
                if rank_likes[score_number] == rank_likes[score_number-1] and score_number < 100:
                    end_string = '\n'.join([end_string,
                                            'Tied {} - {} - {}'.format(score_number, score, user_name)])
                else:
                    end_string = '\n'.join([end_string,
                                            '{} - {} - {}'.format(score_number, score, user_name)])
                tied_score = score
        except IndexError:
            pass
    return end_string


def writealltime():
    ''' Writes the monthly post ids to the all time post ids. '''
    f2 = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'r')
    f3 = open(sys.path[0] + '/../postids/postidsalltime.txt', 'a')
    for line in f2:
        f3.write(line)
    f2.close()
    f3.close()

def writemonthly():
    ''' Writes the bimonthly post ids to the monthly post ids. '''
    f1 = open(sys.path[0] + '/../postids/postids.txt', 'r')
    f2 = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'a')
    for line in f1:
        f2.write(line)
    f1.close()
    f2.close()

def deletecurrent():
    ''' Empties the postids.txt file. '''
    f = open(sys.path[0] + '/../postids/postids.txt', 'w')
    f.write('')
    f.close()

def deletemonthly():
    ''' Empties the postidsmonthly.txt file. '''
    f = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'w')
    f.write('')
    f.close()

def cleanpostids():
    ''' Removes any duplicate ids which may have arisen from testing '''
    f1 = open(sys.path[0] + '/../postids/postidsmonthly.txt', 'r')
    f2 = open(sys.path[0] + '/../postids/postids.txt', 'r')
    postids = set()
    postidsmonthly = set()
    for line in f2:
        postids.add(line.replace('\n', ''))
    for line in f1:
        postid = line.replace('\n', '')
        if postid not in postids:
            postidsmonthly.add(postid)
    f1.close()
    f2.close()
    
    with open(sys.path[0]+'/../postids/postidsmonthly.txt', 'w') as f1:
        for postid in postidsmonthly:
            f1.write(postid + '\n')
    
