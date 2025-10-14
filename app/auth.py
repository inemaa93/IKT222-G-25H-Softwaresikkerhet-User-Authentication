from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from app.db import get_db_connection
from app.bruteforce import init_table, is_locked, record_failed, reset_attempts
from app import totp as totp_utils


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
    totp_code = (data.get("totp") or "").strip()

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
        return jsonify({"error": "locked_out", "message": f"Too many failed attempts. Try again in {int(remaining)} seconds."}), 403

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, totp_secret, totp_enabled FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()

    if not user or not bcrypt.check_password_hash(user["password_hash"], password):
        try:
            record_failed(username, ip)
        except Exception:
            pass
        return jsonify({"error": "Invalid username or password"}), 401

    if user["totp_enabled"]:
        if not totp_code:
            return jsonify({"error": "totp_required", "message": "Two-factor code required"}), 401

        if not user["totp_secret"] or not totp_utils.verify_totp(user["totp_secret"], totp_code):
            try:
                record_failed(username, ip)
            except Exception:
                pass
            return jsonify({"error": "Invalid username, password or totp"}), 401


    try:
        reset_attempts(username, ip)
    except Exception:
        pass

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify({"message": "Login successful", "user": user["username"]}), 200

def _require_login():
    if "user_id" not in session:
        return False, jsonify({"error": "authentication_required"}), 401
    return True, None, None

@auth_bp.route("/2fa/setup", methods=["POST"])
def totp_setup():
    """
    Generate a secret and provisioning URI + QR for the logged-in user.
    Returns: { "secret": "...", "provisioning_uri":"...", "qr": "data:image/png;base64,..." }
    Caller must confirm the code by calling /2fa/confirm with the code.
    """
    ok, resp, status = _require_login()
    if not ok:
        return resp, status

    username = session.get("username")
    secret = totp_utils.generate_totp_secret()
    provisioning_uri = totp_utils.get_provisioning_uri(username, secret)
    qr_png_b64 = totp_utils.generate_qr_base64(provisioning_uri)

    session["pending_totp_secret"] = secret

    return jsonify({
        "secret": secret,
        "provisioning_uri": provisioning_uri,
        "qr": qr_png_b64
    }), 200


@auth_bp.route("/2fa/confirm", methods=["POST"])
def totp_confirm():
    """
    Confirm the TOTP code for the logged-in user and enable 2FA.
    Request body: { "code": "123456" }
    """
    ok, resp, status = _require_login()
    if not ok:
        return resp, status

    data = request.get_json() or {}
    code = (data.get("code") or "").strip()
    if not code:
        return jsonify({"error": "code_required"}), 400

    secret = session.get("pending_totp_secret")
    if not secret:
        return jsonify({"error": "no_pending_setup", "message": "Call /2fa/setup first"}), 400

    if not totp_utils.verify_totp(secret, code):
        return jsonify({"error": "invalid_code"}), 400

    # Save secret and enable 2FA in users table
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET totp_secret=?, totp_enabled=1 WHERE username=?", (secret, session.get("username")))
    conn.commit()
    conn.close()

    # cleanup temp secret
    session.pop("pending_totp_secret", None)

    return jsonify({"message": "2FA enabled"}), 200


@auth_bp.route("/2fa/disable", methods=["POST"])
def totp_disable():
    """
    Disable 2FA for the logged-in user (requires password + totp to confirm in real apps).
    For demo simplicity we require login only.
    """
    ok, resp, status = _require_login()
    if not ok:
        return resp, status

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET totp_secret=NULL, totp_enabled=0 WHERE username=?", (session.get("username"),))
    conn.commit()
    conn.close()

    return jsonify({"message": "2FA disabled"}), 200
