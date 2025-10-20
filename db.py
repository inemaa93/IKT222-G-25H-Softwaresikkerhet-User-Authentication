# db.py
import sqlite3

def init_db():
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema = f.read()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Database initialized with schema.sql")
