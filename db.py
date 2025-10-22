import sqlite3
import os

# Finn absolutt bane til db.py
base_dir = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(base_dir, 'schema.sql')
db_path = os.path.join(base_dir, 'users.db')


def init_db():
    """Initialiser databasen fra schema.sql"""
    print(f" Leser schema fra: {schema_path}")
    print(f" Oppretter database på: {db_path}")

    # Sjekk at schema.sql finnes
    if not os.path.exists(schema_path):
        print("  Fant ikke schema.sql! Sørg for at den ligger i samme mappe som db.py.")
        return

    # Les og kjør schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()

    if not schema.strip():
        print("  schema.sql er tom!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("  Database initialized with schema.sql")


def get_db_connection():
    """Opprett en tilkobling til databasen for Flask"""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  
    return conn


if __name__ == "__main__":
    init_db()
