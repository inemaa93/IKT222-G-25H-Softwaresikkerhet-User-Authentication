import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()
print("\nRegistered users:\n------------------")
for row in cur.execute("SELECT id, username, created_at FROM users"):
    print(f"{row[0]} | {row[1]} | {row[2]}")
conn.close()
