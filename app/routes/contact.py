from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(prefix="/api/contact", tags=["Contact"])


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    phone: Optional[str] = None


@router.post("/send")
def send_contact_message(contact: ContactMessage):

    if len(contact.message) < 10:
        raise HTTPException(status_code=400, detail="Message must be at least 10 characters long")

    return {
        "message": "Contact message received successfully",
        "name": contact.name,
        "email": contact.email,
        "subject": contact.subject
    }


@router.get("/info")
def get_contact_info():
    return {
        "company": "Watera Plus",
        "email": "info@wateraplus.com",
        "phone": "+91-9876543210",
        "address": "Chennai, Tamil Nadu",
        "business_hours": "9:00 AM - 6:00 PM"
    }