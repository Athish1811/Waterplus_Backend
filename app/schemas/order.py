from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    product_id: int
    quantity: int
    delivery_address: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = None
    delivery_address: Optional[str] = None

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

class OrderDetailResponse(OrderResponse):
    product_name: Optional[str] = None
    customer_name: Optional[str] = None
