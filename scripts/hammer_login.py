import os, time, sys, requests

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:5000")
USERNAME = os.environ.get("USERNAME", "bob")
PASSWORD = os.environ.get("PASSWORD", "MyStrongPa55")
WRONG_PW = os.environ.get("WRONG_PW", "badpass")
ATTEMPTS = int(os.environ.get("ATTEMPTS", "3"))
PAUSE_S = float(os.environ.get("PAUSE_S", "0.5"))

def post_login(username, password):
    url = f"{BASE}/login"
    try:
        r = requests.post(url, json={"username": username, "password": password}, timeout=5)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

def main():
    print(f"[+] Target: {BASE}")
    print(f"[+] Username: {USERNAME}")
    print(f"[+] Sending {ATTEMPTS} failed login attempts (pause {PAUSE_S}s) ...")
    for i in range(1, ATTEMPTS + 1):
        pw = WRONG_PW + str(i)
        status, body = post_login(USERNAME, pw)
        print(f"  Attempt {i}: status={status} body={body}")
        time.sleep(PAUSE_S)

    print("\n[+] One more attempt.")
    status, body = post_login(USERNAME, WRONG_PW + "X")
    print(f"  After threshold: status={status} body={body}")

    if status == 403 or (body and "locked_out" in body):
        print("Lockout behavior found.")
    else:
        print("Test failed.")
        # still attempt correct login to show outcome
    print("\n[+] Now try a correct login (may be locked out):")
    status, body = post_login(USERNAME, PASSWORD)
    print(f"  Correct login attempt: status={status} body={body}")

    if status == 200:
        print("Correct login succeeded.")
        sys.exit(0)
    elif status == 403:
        print("Correct login blocked by lockout.")
        sys.exit(0)
    else:
        print("Something went wrong.")
        sys.exit(2)

if __name__ == "__main__":
    main()