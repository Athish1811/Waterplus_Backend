from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserUpdate

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


# 🔥 GET ALL USERS
@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).all()
    return users


# 🔥 GET CURRENT LOGGED IN USER  (IMPORTANT FIX)
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# 🔥 GET USER BY ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.put("/me", response_model=UserResponse)
def update_my_profile(
    updated_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if updated_data.name is not None:
        current_user.name = updated_data.name

    if updated_data.phone is not None:
        current_user.phone = updated_data.phone

    if updated_data.address is not None:
        current_user.address = updated_data.address

    db.commit()
    db.refresh(current_user)

    return current_user
