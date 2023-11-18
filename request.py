import connect_bd
import pandas as pd
import plotly.express as px

cur = connect_bd.getBD()
conn = connect_bd.getConBD()





name_tmp = cur.execute("select name,name from player where teamName ='T1' ")
name_tmp = name_tmp.fetchall()
name_tmp = dict(name_tmp)

match = cur.execute("SELECT distinct teamOne,teamTwo,matchId FROM Match;")
match = match.fetchall()

#Get Name the name of the player with a MatchUrn
def getName():
    name = cur.execute(
    "select distinct P.name as name,M.matchId as matchUrn from match M, player P, team T where P.teamName = T.name")
    name = pd.DataFrame(name, columns=['name', 'matchUrn'])

    return name

#Get all the team

def getTeam():
    sql_queryTeam = pd.read_sql('select distinct MatchId, teamOne, teamTwo from match', conn)
    team = pd.DataFrame(sql_queryTeam, columns=['MatchId', 'teamOne', 'teamTwo', ])
    return team

#Get the stats from the player for every game
def getStats():
    sql_query = pd.read_sql('select name,totalGold, matchUrn,current from StatsPlayer;', conn)
    df = pd.DataFrame(sql_query, columns=['name', 'totalGold', 'matchUrn', 'current', ])
    return df

#get the KP by player
def getKP():
    sql_query2 = pd.read_sql("select name, team , current , matchUrn,SUM(kill+assist) as KP from StatsPlayer group by name, team,current, matchUrn",
        conn)
    df2 = pd.DataFrame(sql_query2, columns=['name', 'team', 'current', 'matchUrn', 'KP'])
    return df2

#get the currentPos
def getCurrentPosOfAction():
    sql_query3 = pd.read_sql("select name , namePlayer, posx,posy, current , matchUrn from Action ;", conn)
    df3 = pd.DataFrame(sql_query3, columns=['name', 'namePlayer', 'posx', 'posy', 'current', 'matchUrn'])
    return df3

#get the matchUrn and the current fro match
def getMatchAndCurrent():
    sql_query4 = pd.read_sql("select MatchId,current from Match", conn)
    df4 = pd.DataFrame(sql_query4, columns=['MatchId', 'current'])
    return df4

def getNameTmp():
    return name_tmp

def getMatch():
    return match