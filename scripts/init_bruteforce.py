import os
import sys

# Ensure project root is on sys.path (so "import app" works when this script is run)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.bruteforce import init_table

if __name__ == "__main__":
    init_table()
    print("failed_logins table created (or already exists).")
