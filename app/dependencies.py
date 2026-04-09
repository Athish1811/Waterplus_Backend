from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User


logger = logging.getLogger("wateraplus.dependencies")

# OAuth2 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current authenticated user"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            logger.error("Token missing 'sub'")
            raise credentials_exception

    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        logger.error(f"User not found for ID: {user_id}")
        raise credentials_exception

    return user