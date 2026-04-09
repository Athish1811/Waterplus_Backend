from typing import Optional, Tuple


# =========================
# PASSWORD VALIDATION
# =========================

def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"

    return True, None


# =========================
# PHONE VALIDATION
# =========================

def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """Validate phone number format"""

    phone_digits = "".join(filter(str.isdigit, phone))

    if len(phone_digits) < 10:
        return False, "Phone number must contain at least 10 digits"

    if len(phone_digits) > 15:
        return False, "Phone number must contain at most 15 digits"

    return True, None