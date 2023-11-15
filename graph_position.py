import pandas as pd
import plotly.express as px
import connect_bd
conn = connect_bd.getConBD()

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
        tmp_limit = 2500
        for x,y,gt,n,curr,urn in (pos[(pos['current'] == k) & (pos['name'] == p)].values):

            if (int(gt) >= int(tmp_limit)) :
                tmp_limit += 2500
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



final_pos = pd.DataFrame(final_pos)

final_pos['gameTime'] = pd.to_datetime(final_pos['gameTime'], unit='ms').dt.time

def getGraphPos():
    return final_pos

def getGraphPosTMP():
    return final_pos[(final_pos['current'] == "1")]