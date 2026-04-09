from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, TokenResponse
from app.utils.validators import validate_password

logger = logging.getLogger("wateraplus.auth")

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):

    # validate password
    is_valid, error_msg = validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # check existing user
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        phone=user_data.phone,
        address=user_data.address,
        role=UserRole.USER
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # create token
    token = create_access_token({
        "sub": str(new_user.id),
        "email": new_user.email,
        "role": new_user.role.value
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=new_user.id,
        email=new_user.email,
        role=new_user.role.value
    )


@router.post("/login", response_model=TokenResponse)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        role=user.role.value
    )