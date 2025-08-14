from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal
from datetime import datetime
import re

# ---------------------------
# Auth Models
# ---------------------------

class UserSignup(BaseModel):
    """
    Schema for new user registration
    """
    name: str = Field(..., min_length=2, max_length=50, description="Full name of the user")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128, description="Strong password")
    role: Literal["user", "admin"] = "user"  # Optional role field with default value

    @validator("name")
    def clean_name(cls, value: str) -> str:
        return value.strip()

    @validator("email")
    def clean_email(cls, value: str) -> str:
        return value.strip().lower()

    @validator("password")
    def validate_password_strength(cls, value: str) -> str:
        """
        Enforces strong password rules:
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value


class UserLogin(BaseModel):
    """
    Schema for user login
    """
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="User account password")

    @validator("email")
    def clean_email(cls, value: str) -> str:
        return value.strip().lower()


class UserResponse(BaseModel):
    """
    Schema for sending user details back to client
    """
    id: str
    name: str
    email: EmailStr
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
# ---------------------------
# Notes / AI Request Models
# ---------------------------

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    ai_enhance: Optional[bool] = True

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    enhanced_content: Optional[str] = None
    created_at: datetime
