from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime


# =========================
# BASE
# =========================

class OrderBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    delivery_address: str = Field(..., min_length=5)

    # 🔥 REQUIRED while creating order
    name: str = Field(..., min_length=2)
    phone: constr(pattern="^[0-9]{10}$")


# =========================
# CREATE
# =========================

class OrderCreate(OrderBase):
    pass


# =========================
# UPDATE
# =========================

class OrderUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = Field(None, gt=0)
    delivery_address: Optional[str] = Field(None, min_length=5)
    status: Optional[str] = None


# =========================
# RESPONSE
# =========================

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    delivery_address: str

    # 🔥 FIX: optional (avoid crash for old DB data)
    name: Optional[str] = None
    phone: Optional[str] = None

    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# DETAIL RESPONSE
# =========================

class OrderDetailResponse(OrderResponse):
    product_name: Optional[str] = None
    customer_name: Optional[str] = None