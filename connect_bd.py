import sqlite3
from sqlite3 import Error
conn = None
cur = None
try :
    conn = sqlite3.connect("tab.db")
    cur = conn.cursor()
except Error as e :
    print(e)

def getBD():
    return cur

def getConBD():
    return conn