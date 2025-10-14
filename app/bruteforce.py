# app/bruteforce.py
import sqlite3
from datetime import datetime, timedelta

DB = "users.db"
MAX_ATTEMPTS = 3
LOCKOUT_MINUTES = 5

def _conn():
    return sqlite3.connect(DB)

def init_table():
    """Create table; run once at setup."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS failed_logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            ip TEXT,
            attempts INTEGER DEFAULT 0,
            last_attempt TEXT
        )
    """)
    conn.commit()
    conn.close()

def record_failed(username, ip):
    """Increase attempt count (or create row) and update timestamp."""
    now = datetime.utcnow().isoformat()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, attempts, last_attempt FROM failed_logins WHERE username=? AND ip=?", (username, ip))
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO failed_logins (username, ip, attempts, last_attempt) VALUES (?, ?, ?, ?)",
                    (username, ip, 1, now))
    else:
        _id, attempts, last = row
        # if last attempt was long ago, reset attempts to 1
        try:
            last_dt = datetime.fromisoformat(last)
        except Exception:
            last_dt = datetime.utcnow()
        if (datetime.utcnow() - last_dt) > timedelta(minutes=LOCKOUT_MINUTES):
            attempts = 1
        else:
            attempts = attempts + 1
        cur.execute("UPDATE failed_logins SET attempts=?, last_attempt=? WHERE id=?", (attempts, now, _id))
    conn.commit()
    conn.close()

def reset_attempts(username, ip):
    """Clear stored attempts for this username+ip."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM failed_logins WHERE username=? AND ip=?", (username, ip))
    conn.commit()
    conn.close()

def is_locked(username, ip):
    """
    Return (locked:bool, seconds_remaining:int|None).
    Locked if attempts >= MAX_ATTEMPTS and last_attempt within LOCKOUT_MINUTES.
    """
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT attempts, last_attempt FROM failed_logins WHERE username=? AND ip=?", (username, ip))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False, None
    attempts, last = row
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return False, None
    elapsed = datetime.utcnow() - last_dt
    if attempts >= MAX_ATTEMPTS and elapsed < timedelta(minutes=LOCKOUT_MINUTES):
        remaining = int((timedelta(minutes=LOCKOUT_MINUTES) - elapsed).total_seconds())
        return True, remaining
    return False, None
