import sqlite3

conn = sqlite3.connect("budget.db")

cursor = conn.cursor()

with conn:
    cursor.execute("DROP TABLE IF EXISTS Debit")
    cursor.execute("CREATE TABLE Debit(Year INT, Month TEXT, Day TEXT, Amnt REAL, Desc TEXT, Note TEXT)")
    cursor.execute("DROP TABLE IF EXISTS Credit")
    cursor.execute("CREATE TABLE Credit(Year INT, Month TEXT, Day TEXT, Amnt REAL, Desc TEXT, Note TEXT)")

if conn:
    conn.close()