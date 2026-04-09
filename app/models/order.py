from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base


# =========================
# ORDER STATUS ENUM
# =========================

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# =========================
# ORDER MODEL
# =========================

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Order Details
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    delivery_address = Column(String(500), nullable=False)

    # Status
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ORM Relationships
    user = relationship("User", back_populates="orders")
    product = relationship("Product")