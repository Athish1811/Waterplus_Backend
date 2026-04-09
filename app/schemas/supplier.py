from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None


# =========================
# CREATE
# =========================

class SupplierCreate(SupplierBase):
    pass


# =========================
# UPDATE
# =========================

class SupplierUpdate(SupplierBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


# =========================
# RESPONSE
# =========================

class SupplierResponse(SupplierBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True