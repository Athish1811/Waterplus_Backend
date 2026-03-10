from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(prefix="/api/contact", tags=["Contact"])

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str

@router.post("/send")
def send_contact_message(contact: ContactMessage):
    """Send contact form message"""
    
    # Validate message length
    if len(contact.message) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message must be at least 10 characters long"
        )
    
    # In production, you would:
    # 1. Save to database
    # 2. Send email notification
    # 3. Send confirmation email to user
    
    return {
        "message": "Contact message received successfully",
        "data": {
            "name": contact.name,
            "email": contact.email,
            "subject": contact.subject,
        }
    }

@router.get("/info")
def get_contact_info():
    """Get company contact information"""
    return {
        "company": "Watera Plus",
        "email": "info@wateraplus.com",
        "phone": "+91-9876543210",
        "address": "Chennai, Tamil Nadu",
        "business_hours": "9:00 AM - 6:00 PM",
        "support_email": "support@wateraplus.com",
    }
