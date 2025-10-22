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

..                                                                                                               [100%]
2 passed, 7 warnings

---

🧱 Databasestruktur

Kolonne	Type	Beskrivelse

id	INTEGER	Primærnøkkel

username	TEXT	Brukernavn

password_hash	TEXT	Hashet passord

created_at	TIMESTAMP	Opprettelsestid

🧰 Ekstra funksjonalitet

🔐 Brute-force Protection

Det finnes to brukere (Bob og Alice), men du kan også registrere nye.

Etter tre feil innloggingsforsøk blir brukeren låst i en tidsperiode.

Før du tester dette, kjør:

python .\scripts\add_totp_columns.py

---

📱 Two-Factor Authentication (2FA)

Start Flask-serveren:

python run.py


Åpne en ny PowerShell og kjør:

python .\scripts\test_2fa_bob.py


Du får da opp QR-kode og kan teste 2FA-flyten.

---

🔑 OAuth2

Når du får en code fra URL-en, har du ~30 sekunder før den utløper.

Start med:

python oauth_demo.py


Besøk deretter:

http://localhost:5000/auth?client_id=demo-client-id&redirect_uri=http://localhost:5000/callback&state=xyz


Kopier koden fra URL-en (mellom code= og &state) og bruk den:

curl.exe -X POST -d "code=THE_CODE" -d "client_id=demo-client-id" -d "client_secret=demo-client-secret" -d "redirect_uri=http://localhost:5000/callback" http://localhost:5000/token


Hvis alt fungerer, får du et access_token, token_type, og expires_in.

---

✅ Dette prosjektet ble gjennomført med hjelp av ChatGPT.







