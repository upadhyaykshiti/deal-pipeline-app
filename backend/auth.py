from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET = "SUPER_SECRET_KEY"
ALGO = "HS256"

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(p: str) -> str:
    return pwd.hash(p)

def verify_pw(p: str, h: str) -> bool:
    return pwd.verify(p, h)

def create_token(user):
    payload = {
        "sub": str(user.id),      # ✅ MUST BE STRING
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }

    token = jwt.encode(payload, SECRET, algorithm=ALGO)
    return token
