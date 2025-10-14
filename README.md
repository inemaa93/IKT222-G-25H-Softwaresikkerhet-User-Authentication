# 🔐 Auth Project – Ine

Dette prosjektet er et Flask-basert autentiseringssystem som håndterer registrering, innlogging og passordhashing.

Prosjektet er delt mellom flere personer – **Person A** (Ine) har ansvaret for å sette opp grunnstrukturen og backend-funksjonaliteten.

---

## 👩‍💻 Ine – Ansvarsområde

Person A har gjort følgende:

- Opprettet prosjektstruktur og aktivert virtuelt miljø (`.venv`)
- Installert og konfigurert Flask
- Opprettet SQLite-database (`users.db`) med tabellen `users`
- Implementert register- og login-endepunkter
- Sørget for at passord lagres sikkert med `bcrypt`
- Testet API-endepunkter i PowerShell med `Invoke-RestMethod`
- Opprettet `.env.example` og README.md for dokumentasjon

---

⚙️ Oppsett lokalt
1. Klon prosjektet
bash
git clone https://github.com/USERNAME/auth-project.git
cd auth-project

2. Aktiver virtuelt miljø (Windows) Powershell
python -m venv .venv
.venv\Scripts\Activate.ps1

3. Installer avhengigheter
pip install flask bcrypt

4. Initialiser databasen
python app\db.py

Da skal det komme:
✅ Database initialized.

🚀 Kjør Flask-serveren
python run.py

Serveren er på:
http://127.0.0.1:5000

🧩 Test API-endepunktene - Dette gjøres på en ny powershell inne i riktig fil mens den første powershellen har oppe Flask-serveren
🔸 Registrer bruker

Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/register" 
  -Headers @{ "Content-Type" = "application/json" } 
  -Body {"username":"alice","password":"S3kretPa55"}

Du skal få følgende beskjed:

message
-------
User registered successfully

🔸 Logg inn bruker
Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/login" 
  -Headers @{ "Content-Type" = "application/json" } 
  -Body {"username":"alice","password":"S3kretPa55"}

Da skal du få fælgende tilbakemelding:

message          user
-------          ----
Login successful alice

---

🗃️ Databasestruktur

| Kolonne       | Type      | Beskrivelse     |
| ------------- | --------- | --------------- |
| id            | INTEGER   | Primærnøkkel    |
| username      | TEXT      | Brukernavn      |
| password_hash | TEXT      | Hashet passord  |
| created_at    | TIMESTAMP | Opprettelsestid |


---


## Brute-force Protection
There are currently two users available, Bob and Alice, but you can also create a new user before testing this out. After choosing a user, attempt to log in to this user with the wrong password three times. This will lock the user out for a certain amount of time, and is visible through a message if a new log-in is attempted. 

## Two-Factor Authentication
Start the project in .venv and write: python run.py
- This starts the Flask server

Open a second Powershell window and write: python .\scripts\test_2fa_bob.py
- This will allow you to try 2fa

## OAuth2
- Quick reminder, when you get the code from the URL, you have roughly 30 seconds to finish the process before the code becomes invalid. If it becomes invalid, restart the process to get a new code.

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





