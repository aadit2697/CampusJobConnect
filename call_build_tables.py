import sqlite3

conn= sqlite3.connect("proj.db")


cursor= conn.cursor()

#open the sql script
with open('build_tables.sql', mode='r') as file:
    sql_script = file.read()

try:
    cursor.executescript(sql_script)

except Exception as e:
    print(e)

cursor.close()
conn.close()