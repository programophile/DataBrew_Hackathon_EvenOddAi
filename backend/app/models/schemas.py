"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional


# Authentication Schemas
class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str
    full_name: str


class AuthResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str


# Settings Schemas
class ProfileUpdate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    role: str


class ShopDetailsUpdate(BaseModel):
    shopName: str
    address: str
    city: str
    postal: str
    shopPhone: str
    shopEmail: str
    hours: str


class NotificationPreferences(BaseModel):
    email: bool
    sms: bool
    push: bool
    lowStock: bool
    salesReports: bool
    staffAlerts: bool


class PasswordChange(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str
