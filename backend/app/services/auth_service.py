"""
Authentication Service
Handles all authentication-related business logic
"""
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import secrets
from typing import Optional

from ..models.auth import User, Session
from ..models.schemas import LoginRequest, SignupRequest, AuthResponse, UserResponse
from ..config.settings import TOKEN_EXPIRY_DAYS


class AuthService:
    """Authentication service for user management"""

    @staticmethod
    def generate_token() -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)

    @staticmethod
    async def login(login_data: LoginRequest) -> AuthResponse:
        """
        Authenticate user with credentials

        Args:
            login_data: LoginRequest with email and password

        Returns:
            AuthResponse with token and user data

        Raises:
            HTTPException: If credentials are invalid
        """
        print(f"Login attempt - Email: {login_data.email}, Password: {login_data.password}")

        # Get user by email
        user = User.get_by_email(login_data.email)

        if not user or not User.verify_password(user, login_data.password):
            print("Authentication FAILED - Invalid credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        print("Authentication SUCCESSFUL")

        # Generate token and create session
        token = AuthService.generate_token()
        expires_at = datetime.now() + timedelta(days=TOKEN_EXPIRY_DAYS)

        Session.create(user, token, expires_at)

        return AuthResponse(
            success=True,
            message="Login successful",
            token=token,
            user=User.get_user_data(user)
        )

    @staticmethod
    async def signup(signup_data: SignupRequest) -> AuthResponse:
        """
        Signup not allowed - only admin user exists

        Raises:
            HTTPException: Always raises forbidden error
        """
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Registration is not allowed. Please use admin credentials."
        )

    @staticmethod
    async def verify_token(token: str) -> dict:
        """
        Verify token and return user info

        Args:
            token: Authentication token

        Returns:
            User data dictionary

        Raises:
            HTTPException: If token is invalid or expired
        """
        if not Session.is_valid(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        user = Session.get_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        return user

    @staticmethod
    async def logout(token: str) -> dict:
        """
        Logout user by removing token

        Args:
            token: Authentication token to invalidate

        Returns:
            Success message
        """
        Session.delete(token)
        return {"success": True, "message": "Logged out successfully"}

    @staticmethod
    async def get_profile(token: str) -> UserResponse:
        """
        Get current user profile

        Args:
            token: Authentication token

        Returns:
            UserResponse with user profile data

        Raises:
            HTTPException: If token is invalid
        """
        user = await AuthService.verify_token(token)

        return UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"]
        )
