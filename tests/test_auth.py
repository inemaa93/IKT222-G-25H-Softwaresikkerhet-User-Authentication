import json
from run import app
from db import init_db

def setup_module(module):
    # Initialiser database før testene kjøres
    init_db()

def test_register_and_login():
    client = app.test_client()

    # Registrer ny bruker
    resp = client.post("/register", json={"username": "testuser", "password": "Passord123"})
    assert resp.status_code in (200, 201)

    # Login med riktig passord
    resp = client.post("/login", json={"username": "testuser", "password": "Passord123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Login successful"

def test_login_wrong_password():
    client = app.test_client()
    resp = client.post("/login", json={"username": "testuser", "password": "WrongPass"})
    assert resp.status_code == 401
