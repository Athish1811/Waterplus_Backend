from typing import Optional

def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    
    return True, None

def validate_phone(phone: str) -> tuple[bool, Optional[str]]:
    """Validate phone number format"""
    phone_digits = ''.join(filter(str.isdigit, phone))
    
    if len(phone_digits) < 10:
        return False, "Phone number must contain at least 10 digits"
    
    if len(phone_digits) > 15:
        return False, "Phone number must contain at most 15 digits"
    
    return True, None
