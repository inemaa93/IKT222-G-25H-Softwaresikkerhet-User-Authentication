import os
from cryptography.fernet import Fernet, InvalidToken

FERNET_KEY = os.environ.get("FERNET_KEY")

if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY environment variable is required")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_secret(plaintext: str) -> str:
    """Return base64-encoded ciphertext (str) for storage in DB."""
    token = fernet.encrypt(plaintext.encode())
    return token.decode()

def decrypt_secret(token_b64: str) -> str | None:
    """Return decrypted plaintext or None if decryption fails."""
    try:
        pt = fernet.decrypt(token_b64.encode())
        return pt.decode()
    except InvalidToken: