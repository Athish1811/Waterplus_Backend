from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    size_liters: float
    price: float
    stock_quantity: Optional[int] = 0


# =========================
# CREATE
# =========================

class ProductCreate(ProductBase):
    pass


# =========================
# UPDATE
# =========================

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    size_liters: Optional[float] = None
    price: Optional[float] = None


# =========================
# RESPONSE
# =========================

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True