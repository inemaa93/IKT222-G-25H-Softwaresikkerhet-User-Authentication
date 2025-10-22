import requests
import pyotp
import json
import base64
import os
import sqlite3

BASE = "http://127.0.0.1:5000"
USERNAME = "admin"
PASSWORD = "admin"

print("  Logging in to create session...")
s = requests.Session()
r = s.post(BASE + "/login", json={"username": USERNAME, "password": PASSWORD})
print("login:", r.status_code, r.text)

# Hvis login krever TOTP, hent fra databasen og prøv igjen
if r.status_code == 401 and "totp_required" in r.text:
    print("  TOTP required — henter secret fra databasen...")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT totp_secret FROM users WHERE username = ?", (USERNAME,))
    row = cursor.fetchone()
    conn.close()

    if not row or not row[0]:
        raise SystemExit("Fant ingen TOTP-secret for brukeren 'admin' — kjør /2fa/setup først.")
    
    secret = row[0]
    totp_code = pyotp.TOTP(secret).now()
    r = s.post(BASE + "/login", json={"username": USERNAME, "password": PASSWORD, "totp": totp_code})
    print("login-with-totp:", r.status_code, r.text)

if r.status_code != 200:
    print(" Login failed — make sure the user exists and password is correct.")
    raise SystemExit(1)

# Hvis brukeren ikke har aktivert TOTP enda, sett det opp
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("SELECT totp_secret FROM users WHERE username = ?", (USERNAME,))
row = cursor.fetchone()
conn.close()

if not row or not row[0]:
    print("\n  Requesting TOTP setup (gets secret + QR)...")
    r = s.post(BASE + "/2fa/setup")
    print("setup status:", r.status_code)
    if r.status_code != 200:
        print(" Setup failed:", r.text)
        raise SystemExit(1)

    data = r.json()
    secret = data.get("secret")
    qrdata = data.get("qr")
    print("secret:", secret)

    # Optional: save QR image so you can open it locally
    if qrdata and qrdata.startswith("data:image/png;base64,"):
        b64 = qrdata.split(",", 1)[1]
        os.makedirs("scripts", exist_ok=True)
        outpath = os.path.join("scripts", f"{USERNAME}_totp_qr.png")
        with open(outpath, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f" QR saved to: {outpath}")

    code = pyotp.TOTP(secret).now()
    print("\nGenerated code (to confirm):", code)
    r = s.post(BASE + "/2fa/confirm", json={"code": code})
    print("confirm:", r.status_code, r.text)
    if r.status_code != 200:
        print("Confirmation failed.")
        raise SystemExit(1)

else:
    # Hvis brukeren allerede har secret, bruk den
    secret = row[0]

print("\nTesting login with TOTP...")
s2 = requests.Session()
totp_code = pyotp.TOTP(secret).now()
r = s2.post(BASE + "/login", json={"username": USERNAME, "password": PASSWORD, "totp": totp_code})
print("login-with-totp:", r.status_code, r.text)

if r.status_code == 200:
    print("\n✅ Success: 2FA login works correctly!")
else:
    print("\n❌ Failed: Login with TOTP did not return 200")
