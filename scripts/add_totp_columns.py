import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Add columns if they don't exist
try:
    cur.execute("ALTER TABLE users ADD COLUMN totp_secret TEXT DEFAULT NULL")
except Exception:
    pass

try:
    cur.execute("ALTER TABLE users ADD COLUMN totp_enabled INTEGER DEFAULT 0")
except Exception:
    pass

conn.commit()
conn.close()
print("Migrated: totp_secret & totp_enabled added (if not present).")
