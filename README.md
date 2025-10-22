🔐 Auth Project

Dette prosjektet er et Flask-basert autentiseringssystem som håndterer registrering, innlogging, passordhashing og tofaktorautentisering (2FA).

Prosjektet er delt mellom flere personer – Person A (Ine) har ansvaret for å sette opp grunnstrukturen og backend-funksjonaliteten.

---


👩‍💻 Ine – Ansvarsområde

Ine har gjort følgende:

Opprettet prosjektstruktur og aktivert virtuelt miljø (.venv)

Installert og konfigurert Flask

Opprettet SQLite-database (users.db) med tabellen users

Implementert register- og login-endepunkter

Sørget for at passord lagres sikkert med bcrypt

Testet API-endepunkter i PowerShell med Invoke-RestMethod

Opprettet .env.example og README.md for dokumentasjon

Fikset import- og databasepath-feil slik at Flask nå starter riktig

Oppdatert get_db_connection() og db.py

Opprettet seed.py for å legge til admin-bruker automatisk

Lagt til Pillow for QR-kodegenerering (2FA)

Testet hele systemet med pytest – alle tester passerer ✅

---

⚙️ Oppsett lokalt

1️⃣ Klon prosjektet

git clone https://github.com/USERNAME/IKT222-G-25H-Softwaresikkerhet-User-Authentication.git

cd IKT222-G-25H-Softwaresikkerhet-User-Authentication

2️⃣ Aktiver virtuelt miljø (Windows PowerShell)

python -m venv .venv

.venv\Scripts\Activate.ps1

3️⃣ Installer avhengigheter

pip install -r requirements.txt

---


Hvis du ikke har en requirements.txt, kan du opprette den slik:

pip install flask bcrypt qrcode pillow pytest

pip freeze > requirements.txt

---

🗃️ Initialiser databasen

Kjør først:

python db.py

---


Du skal få meldingen:

✅ Database initialized with schema.sql

---


Deretter opprett admin-brukeren:

python seed.py

---


Output:

Admin-bruker 'admin' ble lagt til

---

👤 Standard admin-bruker

Brukernavn: admin
Passord: admin

---

🚀 Start Flask-serveren
python run.py

---


Serveren kjører nå på:
👉 http://127.0.0.1:5000

---

🧩 Test API-endepunktene

Åpne et nytt PowerShell-vindu (mens serveren kjører i det originale Powershell vinduet).

🔸 Registrer bruker
Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/register" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username":"alice","password":"S3kretPa55"}'


Respons:

message
-------
User registered successfully

🔸 Logg inn bruker
Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/login" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username":"alice","password":"S3kretPa55"}'


Respons:

message          user
-------          ----
Login successful alice

---

🧪 Kjøre tester

Etter at Flask-appen kjører som forventet, kan du teste systemet:

pytest -q

---

Forventet resultat:

..[100%]2 passed, 7 warnings

---

🧱 Databasestruktur

Kolonne	Type	Beskrivelse


id	INTEGER	Primærnøkkel

username	TEXT	Brukernavn

password_hash	TEXT	Hashet passord

created_at	TIMESTAMP	Opprettelsestid

---

🧰 Ekstra funksjonalitet

---

## Brute-force Protection

### Before trying out the brute-force protection: 
- Start your virtual server
- Start the Flask application

**In a new virtual server (not the one running the Flask)**
- Add the script `add_topt_columns.py`
   - _Copy + Paste Option:_ python .\scripts\add_totp_columns.py

To test the brute-force functionality, you must have a registered user in your system to test it with. Attempt to log in to a user, but write the wrong password three consecutive times. When you go for attempt number four, you will receive a new message, stating that you are currently locked-out and includes a timer (starts at 5 minutes). Each time you attempt to log in before the timer has run out, you will receive the same message (with an updated timer). Once the timer has run out, your attempt record has been reset, and you may retry logging in.

## Two-Factor Authentication
_Remember, this step won't work if the lock-out timer from the brute-force protection is still active, so either wait or restart the server if needed._

- Start your virtual server
- Start the Flask application

**In a new virtual server (not the one running the Flask)**
- Add the script `test_2fa_bob.py`
  - _Copy + Paste Option:_ .\scripts\test_2fa_bob.py

This will run an automatic test showing the 2FA functionality.

## OAuth2

### Quick Reminder Before Test
- When you get the code from the URL, you have roughly 30 seconds to finish the process before the code becomes invalid. If it becomes invalid, restart the process to get a new code.

First, you must start the .venv, and then write: python oauth_demo.py

Once the demo is running, you can write: http://localhost:5000/auth?client_id=demo-client-id&redirect_uri=http://localhost:5000/callback&state=xyz
- This will give you a new URL containing the code you need for the next part
- REMEMBER! Don't have the Flask server running, as it will block this process

Look at the URL, your code will be between "code=" and "&state". Copy this code, add it to the code below and paste it into the Powershell window:

curl.exe -X POST -d "code=THE_CODE" -d "client_id=demo-client-id" -d "client_secret=demo-client-secret" -d "redirect_uri=http://localhost:5000/callback" http://localhost:5000/token

- Replace "THE_CODE" part with the actual code you have received

If all goes well, you should see an access token, a token type, and an expiration date.

---

✅ Dette prosjektet ble gjennomført med hjelp av ChatGPT










