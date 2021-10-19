import sqlite3

conn = sqlite3.connect("budget.db")

cursor = conn.cursor()
sql = "DELETE FROM debit WHERE Amnt = 10.90"
with conn:
    cursor.execute(sql)



if conn:
    conn.close()