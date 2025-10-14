import pyotp
import qrcode
import io
import base64

ISSUER_NAME = "AuthProject"  # change if you want your app name here

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def get_provisioning_uri(username: str, secret: str, issuer: str = ISSUER_NAME) -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)

def generate_qr_base64(provisioning_uri: str) -> str:
    img = qrcode.make(provisioning_uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"

def verify_totp(secret: str, code: str) -> bool:
    try:
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)
    except Exception:
        return False
