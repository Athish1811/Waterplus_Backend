from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from app.core.config import settings


# =========================
# PASSWORD
# =========================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# =========================
# TOKEN
# =========================

def create_access_token(data: dict, expires: Optional[timedelta] = None) -> str:
    payload = {
        **data,
        "exp": datetime.utcnow() + (
            expires or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None