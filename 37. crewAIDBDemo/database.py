import sqlite3

def getConnection():
    con = sqlite3.connect("./studentsDB.sqlite3",check_same_thread=False)
    cursor = con.cursor()
    return (con,cursor)
