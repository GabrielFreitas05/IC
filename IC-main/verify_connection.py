from db.connection import get_connection

conn = get_connection()
print("foreign_keys =", conn.execute("PRAGMA foreign_keys;").fetchone()[0])
conn.close()
