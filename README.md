# 🔐 Auth Project – Person A (Ine)

Dette prosjektet er et Flask-basert autentiseringssystem som håndterer registrering, innlogging og passordhashing.

Prosjektet er delt mellom flere personer – **Person A** (Ine) har ansvaret for å sette opp grunnstrukturen og backend-funksjonaliteten.

---

## 👩‍💻 Person A – Ansvarsområde

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

✅ Dette prosjektet ble gjennomført med hjelp av ChatGPT





