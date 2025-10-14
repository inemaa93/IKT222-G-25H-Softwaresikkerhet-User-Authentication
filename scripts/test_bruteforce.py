import os, sys
sys.path.insert(0, os.path.abspath('.'))
from app.bruteforce import init_table, record_failed, is_locked
init_table()
# simulate 3 failed attempts from the same IP
record_failed("alice", "127.0.0.1")
record_failed("alice", "127.0.0.1")
record_failed("alice", "127.0.0.1")
locked, rem = is_locked("alice", "127.0.0.1")
print("Module test -> locked:", locked, "remaining_seconds:", rem)
