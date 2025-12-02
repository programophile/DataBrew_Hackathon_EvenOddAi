"""
Settings Controller
Handles HTTP requests for settings-related endpoints
"""
from fastapi import Header, HTTPException
from typing import Optional

from ..models.schemas import ProfileUpdate, ShopDetailsUpdate, NotificationPreferences, PasswordChange
from ..services.auth_service import AuthService


class SettingsController:
    """Controller for settings endpoints"""

    @staticmethod
    async def get_profile_settings(authorization: Optional[str] = Header(None)) -> dict:
        """Get user profile settings"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "firstName": "Sarah",
            "lastName": "Ahmed",
            "email": "admin@gmail.com",
            "phone": "+880 1712-345678",
            "role": "Owner & Manager",
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah"
        }

    @staticmethod
    async def update_profile_settings(profile: ProfileUpdate, authorization: Optional[str] = Header(None)) -> dict:
        """Update user profile settings"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "success": True,
            "message": "Profile updated successfully",
            "profile": profile.dict()
        }

    @staticmethod
    async def get_shop_settings(authorization: Optional[str] = Header(None)) -> dict:
        """Get shop details settings"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "shopName": "DataBrew Coffee House",
            "address": "123 Gulshan Avenue, Dhaka 1212",
            "city": "Dhaka",
            "postal": "1212",
            "shopPhone": "+880 2-9876543",
            "shopEmail": "contact@databrew.com",
            "hours": "8:00 AM - 11:00 PM (Daily)"
        }

    @staticmethod
    async def update_shop_settings(shop: ShopDetailsUpdate, authorization: Optional[str] = Header(None)) -> dict:
        """Update shop details settings"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "success": True,
            "message": "Shop details updated successfully",
            "shop": shop.dict()
        }

    @staticmethod
    async def get_notification_preferences(authorization: Optional[str] = Header(None)) -> dict:
        """Get notification preferences"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "email": True,
            "sms": False,
            "push": True,
            "lowStock": True,
            "salesReports": True,
            "staffAlerts": True
        }

    @staticmethod
    async def update_notification_preferences(preferences: NotificationPreferences, authorization: Optional[str] = Header(None)) -> dict:
        """Update notification preferences"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "success": True,
            "message": "Notification preferences updated successfully",
            "preferences": preferences.dict()
        }

    @staticmethod
    async def change_password(password_data: PasswordChange, authorization: Optional[str] = Header(None)) -> dict:
        """Change user password"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        if password_data.newPassword != password_data.confirmPassword:
            raise HTTPException(status_code=400, detail="New passwords do not match")

        if password_data.currentPassword != "admin123":
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        return {
            "success": True,
            "message": "Password changed successfully"
        }

    @staticmethod
    async def get_active_sessions(authorization: Optional[str] = Header(None)) -> dict:
        """Get active sessions"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "sessions": [
                {
                    "id": 1,
                    "device": "Chrome on Windows",
                    "location": "Dhaka, Bangladesh",
                    "lastActive": "Active now",
                    "isCurrent": True
                },
                {
                    "id": 2,
                    "device": "Mobile App",
                    "location": "Dhaka, Bangladesh",
                    "lastActive": "2 hours ago",
                    "isCurrent": False
                }
            ]
        }

    @staticmethod
    async def logout_session(session_id: int, authorization: Optional[str] = Header(None)) -> dict:
        """Logout a specific session"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "success": True,
            "message": f"Session {session_id} logged out successfully"
        }

    @staticmethod
    async def logout_all_sessions(authorization: Optional[str] = Header(None)) -> dict:
        """Logout all other sessions"""
        user = await AuthService.verify_token(authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {
            "success": True,
            "message": "All other sessions logged out successfully"
        }
