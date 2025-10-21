from flask import Flask, request, redirect, jsonify
import os, secrets, time

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = "demo-client-id"
CLIENT_SECRET = "demo-client-secret"
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_CODES = {}
TOKENS = {}

@app.route("/auth", methods=["GET"])
def auth():
    """
    Step 1: Simulate user granting permission (Authorization Endpoint)
    """
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")
    state = request.args.get("state", "")

    if client_id != CLIENT_ID or redirect_uri != REDIRECT_URI:
        return jsonify({"error": "invalid_client"}), 400

    auth_code = secrets.token_urlsafe(16)
    AUTH_CODES[auth_code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "expires": time.time() + 60
    }

    print(f"[DEBUG] Issued auth code: {auth_code}")

    return redirect(f"{redirect_uri}?code={auth_code}&state={state}")

@app.route("/token", methods=["POST"])
def token():
    """
    Step 2: Client exchanges code for access token (Token Endpoint)
    """
    code = request.form.get("code")
    client_id = request.form.get("client_id")
    client_secret = request.form.get("client_secret")
    redirect_uri = request.form.get("redirect_uri")

    auth_data = AUTH_CODES.get(code)
    if not auth_data or auth_data["expires"] < time.time():
        return jsonify({"error": "invalid_or_expired_code"}), 400

    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        return jsonify({"error": "invalid_client_credentials"}), 401

    if redirect_uri != auth_data["redirect_uri"]:
        return jsonify({"error": "redirect_uri_mismatch"}), 400

    access_token = secrets.token_urlsafe(24)
    TOKENS[access_token] = {
        "client_id": client_id,
        "expires": time.time() + 300
    }

    del AUTH_CODES[code]

    print(f"[DEBUG] Issued access token: {access_token}")
    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 300
    }), 200

@app.route("/protected_resource", methods=["GET"])
def protected_resource():
    """
    Step 3: Access a protected resource using a valid token
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "missing_token"}), 401

    token = auth_header.split(" ")[1]
    token_data = TOKENS.get(token)

    if not token_data or token_data["expires"] < time.time():
        return jsonify({"error": "invalid_or_expired_token"}), 401

    return jsonify({
        "message": "Access granted!",
        "user_info": {
            "name": "OAuth2 Demo User",
            "email": "demo@example.com"
        }
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
