import requests
import pyotp
import json
import base64
import os

BASE = "http://127.0.0.1:5000"
USERNAME = "bob"
PASSWORD = "MyStrongPa55"

s = requests.Session()

print("  Logging in to create session...")
r = s.post(BASE + "/login", json={"username": USERNAME, "password": PASSWORD})
print("login:", r.status_code, r.text)
if r.status_code != 200:
    print(" Login failed — make sure the user exists and password is correct.")
    raise SystemExit(1)

print("\n  Requesting TOTP setup (gets secret + QR)...")
r = s.post(BASE + "/2fa/setup")
print("setup status:", r.status_code)
if r.status_code != 200:
    print(" Setup failed:", r.text)
    raise SystemExit(1)

data = r.json()
print("setup data keys:", list(data.keys()))
secret = data.get("secret")
qrdata = data.get("qr")
print("secret:", secret)

# Optional: save QR image so you can open it locally
if qrdata and qrdata.startswith("data:image/png;base64,"):
    b64 = qrdata.split(",", 1)[1]
    os.makedirs("scripts", exist_ok=True)
    outpath = os.path.join("scripts", f"bob_totp_qr.png")
    with open(outpath, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f" QR saved to: {outpath}")
    print("  Open this image and scan it with Google Authenticator")

#   Confirm using the current code from the secret
code = pyotp.TOTP(secret).now()
print("\nGenerated code (to confirm):", code)
r = s.post(BASE + "/2fa/confirm", json={"code": code})
print("confirm:", r.status_code, r.text)
if r.status_code != 200:
    print("Confirmation failed.")
    raise SystemExit(1)

#   Try a new login that requires totp
print("\nTesting login with TOTP...")
s2 = requests.Session()
totp_code = pyotp.TOTP(secret).now()
r = s2.post(BASE + "/login", json={"username": USERNAME, "password": PASSWORD, "totp": totp_code})
print("login-with-totp:", r.status_code, r.text)

print("\nDone! If the final login returns 200, 2FA works correctly.")
