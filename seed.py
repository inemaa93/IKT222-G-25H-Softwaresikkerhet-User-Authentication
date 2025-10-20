import sqlite3
import bcrypt

# Velg ønsket adminbruker
username = "admin"
password = "Admin1234"  # Husk å endre i produksjon

# Hash passordet med bcrypt
hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Koble til databasen
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Sett inn bruker
c.execute(
    "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
    (username, hashed_pw.decode('utf-8'))
)

conn.commit()
conn.close()
print(f" Admin-bruker '{username}' ble lagt til")
