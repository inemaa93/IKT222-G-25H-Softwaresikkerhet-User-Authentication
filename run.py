from flask import Flask
from app.auth import auth_bp, bcrypt
from app.db import init_db
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.register_blueprint(auth_bp)

bcrypt.init_app(app)

@app.route("/")
def home():
    return {"message": "Authentication API is running"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
