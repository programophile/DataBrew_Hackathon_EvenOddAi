"""
Authentication Routes
Defines API endpoints for authentication
"""
from fastapi import APIRouter, Header
from typing import Optional

from ..models.schemas import LoginRequest, SignupRequest, AuthResponse, UserResponse
from ..controllers.auth_controller import AuthController

router = APIRouter(prefix="", tags=["Authentication"])


@router.post("/login", response_model=AuthResponse)
async def login(login_data: LoginRequest):
    """
    Login with admin credentials

    Email: admin@gmail.com
    Password: admin123

    Returns authentication token for subsequent requests
    """
    return await AuthController.login(login_data)


@router.post("/signup", response_model=AuthResponse)
async def signup(signup_data: SignupRequest):
    """
    Signup endpoint (disabled - only admin user exists)
    """
    return await AuthController.signup(signup_data)


@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """
    Logout current user session
    Requires: Authorization header with Bearer token
    """
    return await AuthController.logout(authorization)


@router.get("/profile", response_model=UserResponse)
async def profile(authorization: Optional[str] = Header(None)):
    """
    Get current user profile
    Requires: Authorization header with Bearer token
    """
    return await AuthController.get_profile(authorization)


@router.get("/verify")
async def verify(authorization: Optional[str] = Header(None)):
    """
    Verify if authentication token is valid
    Requires: Authorization header with Bearer token
    """
    return await AuthController.verify(authorization)
