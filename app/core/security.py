from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


# =========================
# PASSWORD HASHING
# =========================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# =========================
# JWT TOKEN CREATION
# =========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# =========================
# JWT TOKEN DECODE
# =========================

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT access token"""

    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None