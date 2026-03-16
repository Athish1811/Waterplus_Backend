from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, TokenResponse
from app.utils.validators import validate_password, validate_phone
import logging

logger = logging.getLogger("wateraplus.auth")

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""

    # Validate password
    is_valid, error_msg = validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Check password match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"Signup failed: Email already registered ({user_data.email})")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        phone=user_data.phone,
        address=user_data.address,
        role=UserRole.USER  # Always default to USER — never trust client-provided role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(
        f"New user registered: {new_user.email} "
        f"(id={new_user.id}, role={new_user.role.value})"
    )

    # Create access token
    access_token = create_access_token(
        data={
            "sub": str(new_user.id),
            "email": new_user.email,
            "role": new_user.role.value
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        email=new_user.email,
        role=new_user.role.value
    )


@router.post("/login", response_model=TokenResponse)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Login user"""

    # Fetch user by email
    user = db.query(User).filter(User.email == username).first()

    if not user:
        logger.warning(f"Login failed: Invalid email ({username})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(password, user.password):
        logger.warning(f"Login failed: Invalid password for {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    logger.info(f"User logged in: {user.email} (id={user.id}, role={user.role.value})")

    # Create token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        role=user.role.value
    )