import os
import json
from run import app
from db import init_db

def setup_module(module):
    """
    Initialiserer databasen på nytt før testene kjører.
    Dette sikrer at testene alltid kjører på en ren database,
    slik at tidligere brukere ikke skaper '409 Conflict'-feil.
    """
    db_path = "users.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(" Slettet eksisterende database før testkjøring.")
    init_db()  # Lager databasen fra schema.sql

def test_register_and_login():
    client = app.test_client()

    # Registrer ny bruker
    resp = client.post("/register", json={"username": "testuser", "password": "Passord123"})
    print("Register response:", resp.status_code, resp.data)
    assert resp.status_code in (200, 201), f"Feil ved registrering: {resp.status_code} {resp.data}"

    # Login med riktig passord
    resp = client.post("/login", json={"username": "testuser", "password": "Passord123"})
    print("Login response:", resp.status_code, resp.data)
    assert resp.status_code == 200, f"Feil ved login: {resp.status_code} {resp.data}"
    data = resp.get_json()
    assert data["message"] == "Login successful"

def test_login_wrong_password():
    client = app.test_client()

    # Feil passord
    resp = client.post("/login", json={"username": "testuser", "password": "WrongPass"})
    print("Wrong password response:", resp.status_code, resp.data)
    assert resp.status_code == 401
