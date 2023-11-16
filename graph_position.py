import pandas as pd
import plotly.express as px
import connect_bd
conn = connect_bd.getConBD()


Oner = pd.read_sql("select posx, posy, gameTime,name, current,matchUrn from position where name='T1 Oner'and gameTime <= 130000  ", conn)
Oner = pd.DataFrame(Oner, columns=['posx', 'posy', 'gameTime', 'name','current','matchUrn'])


pos = pd.read_sql("select posx, posy, gameTime,name, current,matchUrn from position  ", conn)
pos = pd.DataFrame(pos, columns=['posx', 'posy', 'gameTime', 'name','current','matchUrn'])

pos_posx = []
pos_posy = []
pos_name = []
pos_gameTime =[]
pos_series = []
pos_urn =[]
tmp_limit = 2500

srs = [i for i in pos['current'].unique()]
pos_player = [i for i in pos['name'].unique()]

for k in srs :
    for p in pos_player:
        tmp_limit = 3500
        for x,y,gt,n,curr,urn in (pos[(pos['current'] == k) & (pos['name'] == p)].values):

            if (int(gt) >= int(tmp_limit)) :
                tmp_limit += 3500
                pos_posx.append(x)
                pos_posy.append(y)
                pos_name.append(n)
                pos_gameTime.append(gt)
                pos_series.append(curr)
                pos_urn.append(urn)



final_pos = {
  "posx": pos_posx,
  "posy": pos_posy,
  "name":  pos_name,
   "gameTime" : pos_gameTime,
   "current" : pos_series,
    "matchUrn": pos_urn
}


def getOner():
    pos_posx = []
    pos_posy = []
    pos_name = []
    pos_gameTime = []
    pos_series = []
    pos_urn = []
    req = "select posx,posy,round(gameTime/1000)*1000 as gameTime,name,current,matchUrn from ExactPosition where name='T1 Oner'and gameTime <= 130000"
    pos = pd.read_sql(req, conn)
    pos = pd.DataFrame(pos, columns=['posx', 'posy', 'gameTime', 'name','current','matchUrn'])
    print(pos['gameTime'])



    final_pos = pd.DataFrame(pos)


    return final_pos

def getBegPlayer(player):
    req = "select posx,posy,round(gameTime/1000)*1000 as gameTime,name,current,matchUrn from ExactPosition where name='%s'and gameTime <= 110000 and gameTime >= 45000 " % player
    pos = pd.read_sql(req, conn)
    pos = pd.DataFrame(pos, columns=['posx', 'posy', 'gameTime', 'name', 'current', 'matchUrn'])

    final_pos = pd.DataFrame(pos)

    return final_pos



def getCurrent(current):
    pos_posx = []
    pos_posy = []
    pos_name = []
    pos_gameTime = []
    pos_series = []
    pos_urn = []
    req = "select posx, posy, gameTime,name, current,matchUrn from position where current ='%s'" % current
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





final_pos = pd.DataFrame(final_pos)

final_pos['gameTime'] = pd.to_datetime(final_pos['gameTime'], unit='ms').dt.time

def getGraphPos():
    return pos

def getGraphPosTMP():
    return final_pos[(final_pos['current'] == "1")]