from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
import enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    phone = Column(String(20))
    address = Column(String(500))

    role = Column(Enum(UserRole), default=UserRole.USER)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")