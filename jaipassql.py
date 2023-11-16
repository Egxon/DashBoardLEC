import connect_bd

conn = connect_bd.getConBD()
cur = connect_bd.getBD()
import pandas as pd

sql = "SELECT posx, posy FROM Position"


pos = pd.read_sql("select champName, result from StatsPlayer", conn)
pos = pd.DataFrame(pos, columns=['champName','result'])
print(pos)

WinRate = {}

for name,result in pos.values:
    print(name,result)

    if name not in WinRate.keys():
        WinRate[name]=[result]
    else:
        WinRate[name].append(result)

for key,value in WinRate.items():
    joueur = key

    W = (value.count("W")/len(value) ) *100

    print("Le taux de winrate de", joueur,"est :", W,"%")


print(WinRate)