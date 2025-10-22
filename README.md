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

⚙️ Pillow

**Merk:** prosjektet bruker Pillow for QR-kode-generering (2FA). Hvis ikke Pillow blir nedlastet fra `requirements.txt`, installer det i det aktive virtuelle miljøet:


1. Aktiver `.venv`
   
2. Kjør:
   
powershell

pip install Pillow

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

## 🧪 Automated Testing

The project includes automated tests using **pytest** to verify authentication and login functionality.

Before each test run, the test suite automatically deletes and reinitializes the database (`users.db`) using the schema in `schema.sql`.  
This ensures a clean, isolated environment every time the tests run and prevents `409 Conflict` errors caused by previously registered users.

To run the tests:

bash
pytest -q

---
Expected output:

 Slettet eksisterende database før testkjøring.
 
.. 2 passed in 1.5s

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

### Før du prøver å teste funksjonen: 
- Start din virtuelle server
- Start Flask applikasjonen

**I et nytt virtuelt miljø (ikke den som kjører serveren)**
- Legg til skriptet `add_topt_columns.py`
   - _Copy + Paste:_ python .\scripts\add_totp_columns.py

For å teste brute-force funksjonen må du ha en registrert bruker i systemet. Det ligger allerede en admin bruker på systemet om du har gjort de tidligere stegene, men du kan også lage en ny bruker om ønsket. Forsøk å logg inn på brukeren, men skriv feil passord, og gjør dette tre ganger. Dette trigger "lock-out" funksjonen, og om du forsøker å logge inn igjen får du ikke lov, og du får se timeren på lockouten. Denne varer i 5 minutter før du kan forsøke å logge inn på nytt. 

## Two-Factor Authentication
_Husk, denne delen funker ikke hvis timeren fra brute-force funksjonen fortsatt er aktiv. Enten vent, eller restart serveren før du går videre._

- Start din virtuelle server
- Start Flask applikasjonen

**I et nytt virtuelt miljø (ikke den som kjører serveren)**
- Legg til skriptet `test_2fa_bob.py`
  - _Copy + Paste:_ .\scripts\test_2fa_bob.py

Dette kjører en automatisk test som viser at 2FA funksjonaliteten fungerer som den skal.

## OAuth2

### Viktig informasjon før du kjører testen
- Når du skal hente koden fra URLen, har du ca 30 sekunder på å fullføre resten av prosessen før koden blir avvist. Om den blir avvist må du starte forsøket på nytt og få en ny kode.
- Ikke ha FLask serveren i gang når du forsøker denne delen, da de konflikter med hverandre.

Først må du starte den virtuelle serveren, og skrive: `python oauth_demo.py`

Dette starter en demo, og da må du bruke denne lenken i en browser: http://localhost:5000/auth?client_id=demo-client-id&redirect_uri=http://localhost:5000/callback&state=xyz
- I URLen vil du få en kode som skal brukes til neste del

- I URLen, mellom "code=" og "&state" ligger koden din, og denne skal du sette inn i koden under (bytt det ut med "THE_CODE" delen):

curl.exe -X POST -d "code=THE_CODE" -d "client_id=demo-client-id" -d "client_secret=demo-client-secret" -d "redirect_uri=http://localhost:5000/callback" http://localhost:5000/token

Om alt går som det skal, bør du se en "access token" en "token type" og en "expiration date".

---

✅ Dette prosjektet ble gjennomført med hjelp av ChatGPT













