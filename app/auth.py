from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from app.db import get_db_connection
from app.bruteforce import init_table, is_locked, record_failed, reset_attempts


try:
    init_table()
except Exception:
    pass

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, pw_hash))
        conn.commit()
    except Exception as e:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()
    return jsonify({"message": "User registered successfully"}), 201
    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    ip = request.remote_addr or "local"
    if ip == "::1":
        ip = "127.0.0.1"

    try:
        locked, remaining = is_locked(username, ip)
    except Exception:
        locked, remaining = False, None

    if locked:
        return jsonify({
            "error": "locked_out",
            "message": f"Too many failed login attempts. Try again in {int(remaining)} seconds."
        }), 403

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()

    if not user or not bcrypt.check_password_hash(user["password_hash"], password):
        try:
            record_failed(username, ip)
        except Exception:
            pass
        return jsonify({"error": "Invalid username or password"}), 401

    try:
        reset_attempts(username, ip)
    except Exception:
        pass

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify({"message": "Login successful", "user": user["username"]}), 200
