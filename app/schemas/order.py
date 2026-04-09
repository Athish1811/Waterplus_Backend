from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# BASE
# =========================

class OrderBase(BaseModel):
    product_id: int
    quantity: int
    delivery_address: str


# =========================
# CREATE
# =========================

class OrderCreate(OrderBase):
    pass


# =========================
# UPDATE
# =========================

class OrderUpdate(OrderBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    delivery_address: Optional[str] = None
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