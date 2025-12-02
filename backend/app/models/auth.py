"""
Authentication models
User and Session models for authentication
"""
from datetime import datetime
from typing import Optional

# In-memory user storage (hardcoded admin)
ADMIN_USER = {
    "id": 1,
    "email": "admin@gmail.com",
    "password": "admin123",  # In production, this would be hashed
    "full_name": "Admin User",
    "role": "admin"
}

# In-memory session storage
active_sessions = {}


class User:
    """User model for authentication"""

    @staticmethod
    def get_by_email(email: str) -> Optional[dict]:
        """Get user by email"""
        if email.strip().lower() == ADMIN_USER["email"].lower():
            return ADMIN_USER
        return None

    @staticmethod
    def verify_password(user: dict, password: str) -> bool:
        """Verify user password"""
        return user["password"] == password

    @staticmethod
    def get_user_data(user: dict) -> dict:
        """Get safe user data (without password)"""
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }


class Session:
    """Session model for managing user sessions"""

    @staticmethod
    def create(user: dict, token: str, expires_at: datetime) -> dict:
        """Create a new session"""
        session = {
            "user": User.get_user_data(user),
            "expires_at": expires_at
        }
        active_sessions[token] = session
        return session

    @staticmethod
    def get(token: str) -> Optional[dict]:
        """Get session by token"""
        return active_sessions.get(token)

    @staticmethod
    def delete(token: str) -> bool:
        """Delete session by token"""
        if token in active_sessions:
            del active_sessions[token]
            return True
        return False

    @staticmethod
    def is_valid(token: str) -> bool:
        """Check if session token is valid and not expired"""
        session = Session.get(token)
        if not session:
            return False

        if datetime.now() > session["expires_at"]:
            Session.delete(token)
            return False

        return True

    @staticmethod
    def get_user(token: str) -> Optional[dict]:
        """Get user from session token"""
        session = Session.get(token)
        if session and Session.is_valid(token):
            return session["user"]
        return None
