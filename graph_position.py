import pandas as pd
import plotly.express as px
import connect_bd
conn = connect_bd.getConBD()



def getMoveEarly(player=None):
    if player == None:
        req = "select posx,posy,round(gameTime/1000)*1000 as gameTime,name,current,matchUrn from ExactPosition where name='T1 Oner'and gameTime <= 130000"
    else:
        req = "select posx,posy,round(gameTime/1000)*1000 as gameTime,name,current,matchUrn from ExactPosition where name='%s'and gameTime <= 110000 and gameTime >= 45000 " % player

    pos = pd.read_sql(req, conn)
    pos = pd.DataFrame(pos, columns=['posx', 'posy', 'gameTime', 'name','current','matchUrn'])
    final_pos = pd.DataFrame(pos)
    return final_pos



#Renvoie la dataframe des positions des joueurs durant la game
def getCurrentPos(matchUrn=None,current=None):
    pos_posx = []
    pos_posy = []
    pos_name = []
    pos_gameTime = []
    pos_series = []
    pos_urn = []
    if matchUrn != None and current != None:
        req = "select posx, posy, gameTime,name, current,matchUrn from position where current ='%s' and matchUrn = '%s'" % (current,matchUrn)
        print(req)
    else:

        req = "select posx, posy, gameTime,name, current,matchUrn from position where current ='1' and matchUrn ='esports:match:b3590072-d7dd-4d8c-b307-b671b3760075'"
        print(req)
    pos = pd.read_sql(req, conn)
    pos = pd.DataFrame(pos, columns=['posx', 'posy', 'gameTime', 'name','current','matchUrn'])

    pos_player = [i for i in pos['name'].unique()]

    for p in pos_player :
        tmp_limit = 3500
        for x, y, gt, n, curr, urn in (pos[(pos['name'] == p)].values) :

            if (int(gt) >= int(tmp_limit)) :
                tmp_limit += 3500
                pos_posx.append(x)
                pos_posy.append(y)
                pos_name.append(n)
                pos_gameTime.append(gt)
                pos_series.append(curr)
                pos_urn.append(urn)

    pos = {
        "posx" : pos_posx,
        "posy" : pos_posy,
        "name" : pos_name,
        "gameTime" : pos_gameTime,
        "current" : pos_series,
        "matchUrn" : pos_urn
    }

    final_pos = pd.DataFrame(pos)
    final_pos['gameTime'] = pd.to_datetime(final_pos['gameTime'], unit='ms').dt.time

    return final_pos


#Renvoie la dataframe des positions des joueurs durant la game LNG  vs T1 current 1




def getGraphPos():
    pos = pd.read_sql("select posx, posy, gameTime,name, current,matchUrn from position  ", conn)
    pos = pd.DataFrame(pos, columns=['posx', 'posy', 'gameTime', 'name', 'current', 'matchUrn'])
    return pos

