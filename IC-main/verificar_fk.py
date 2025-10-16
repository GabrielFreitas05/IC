import sqlite3

conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_key_list(process_activities);")
for row in cursor.fetchall():
    print(row)
conn.close()
