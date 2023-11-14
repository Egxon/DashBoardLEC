
import time

import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import sqlite3
from sqlite3 import Error

conn = None
try:
    conn = sqlite3.connect("tab.db")
    cur = conn.cursor()
except Error as e:
    print(e)



def PlayerPosKDA(player):

    reqK = "SELECT posx, posy from Action where namePlayer ='%s' and name ='KILL'" % player
    reqD = "SELECT posx, posy from Action where namePlayer ='%s' and name ='DEATH'" % player
    reqA = "SELECT posx, posy from Action where namePlayer ='%s' and name ='ASSIST'" % player
    title = "Impact of '%s' " % player

    cur.execute(reqK)
    res = cur.fetchall()

    x = [i[0] for i in res]
    y = [i[1] for i in res]

    fig, ax = plt.subplots()
    im = plt.imread("Minimap.jpg")
    plt.scatter(x, y, vmin=0, vmax=15000, s=60, c="tab:green", label='Kill')

    cur.execute(reqD)
    res = cur.fetchall()
    x = [i[0] for i in res]
    y = [i[1] for i in res]
    plt.scatter(x, y, vmin=0, vmax=15000, s=60, c="tab:red", label='Death')

    cur.execute(reqA)
    res = cur.fetchall()
    x = [i[0] for i in res]
    y = [i[1] for i in res]
    plt.scatter(x, y, vmin=0, vmax=15000, s=60, c="tab:orange", label='Assist')

    crs = mplcursors.cursor(ax, hover=True)
    crs.connect("add", lambda sel : sel.annotation.set_text(
        'Point {},{}'.format(sel.target[0], sel.target[1])))
    plt.imshow(im, extent=[0, 15000, 0, 15000])
    plt.title(title)
    plt.legend()

    plt.show()

def totalGold():
    cur.execute("select name,totalGold from StatsPlayer;")
    res = cur.fetchall()

    names = [i[0] for i in res]
    values = [i[1] for i in res]

    plt.figure(figsize=(6, 2))
    plt.title("Total of gold won at the end of the game")
    plt.xlabel('Player')
    plt.ylabel('Total Of Gold')

    plt.bar(names, values, color='gold')
    plt.show()

def KP():

    cur.execute("select name from Player where teamId IN (select teamId from Team where name ='T1')")
    res = cur.fetchall()
    name = [i for i in res]
    KP = []

    for i in name:
        req = "select kill,assist from StatsPlayer where name = '%s' " % i
        cur.execute(req)
        res = cur.fetchall()
        var = int(res[0][0]) + int(res[0][1])
        KP.append(var)


    plt.pie(KP, labels=name,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("KP of T1's Player against LNG ",
              bbox={'facecolor' : '0.8', 'pad' : 5})
    plt.show()




if __name__ == '__main__':
    PlayerPosKDA("T1 Keria")
    totalGold()
    KP()
