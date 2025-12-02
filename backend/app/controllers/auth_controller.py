"""
Authentication Controller
Handles HTTP requests for authentication endpoints
"""
from fastapi import Header, HTTPException
from typing import Optional

from ..models.schemas import LoginRequest, SignupRequest, AuthResponse, UserResponse
from ..services.auth_service import AuthService


class AuthController:
    """Controller for authentication endpoints"""

    @staticmethod
    async def login(login_data: LoginRequest) -> AuthResponse:
        """Handle login request"""
        return await AuthService.login(login_data)

    @staticmethod
    async def signup(signup_data: SignupRequest) -> AuthResponse:
        """Handle signup request"""
        return await AuthService.signup(signup_data)

    @staticmethod
    async def logout(authorization: Optional[str] = Header(None)) -> dict:
        """Handle logout request"""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Missing or invalid authorization header"
            )

        token = authorization.replace("Bearer ", "")
        return await AuthService.logout(token)

    @staticmethod
    async def get_profile(authorization: Optional[str] = Header(None)) -> UserResponse:
        """Handle get profile request"""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Missing or invalid authorization header"
            )

        token = authorization.replace("Bearer ", "")
        return await AuthService.get_profile(token)

    @staticmethod
    async def verify(authorization: Optional[str] = Header(None)) -> dict:
        """Handle token verification request"""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Missing or invalid authorization header"
            )

        token = authorization.replace("Bearer ", "")
        user = await AuthService.verify_token(token)

        return {
            "valid": True,
            "user": user
        }
