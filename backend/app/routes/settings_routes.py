"""
Settings Routes
Defines API endpoints for user and shop settings
"""
from fastapi import APIRouter, Header
from typing import Optional

from ..models.schemas import ProfileUpdate, ShopDetailsUpdate, NotificationPreferences, PasswordChange
from ..controllers.settings_controller import SettingsController

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/profile")
async def get_profile_settings(authorization: Optional[str] = Header(None)):
    """
    Get user profile settings
    """
    return await SettingsController.get_profile_settings(authorization)


@router.put("/profile")
async def update_profile_settings(profile: ProfileUpdate, authorization: Optional[str] = Header(None)):
    """
    Update user profile settings
    """
    return await SettingsController.update_profile_settings(profile, authorization)


@router.get("/shop")
async def get_shop_settings(authorization: Optional[str] = Header(None)):
    """
    Get shop details settings
    """
    return await SettingsController.get_shop_settings(authorization)


@router.put("/shop")
async def update_shop_settings(shop: ShopDetailsUpdate, authorization: Optional[str] = Header(None)):
    """
    Update shop details settings
    """
    return await SettingsController.update_shop_settings(shop, authorization)


@router.get("/notifications")
async def get_notification_preferences(authorization: Optional[str] = Header(None)):
    """
    Get notification preferences
    """
    return await SettingsController.get_notification_preferences(authorization)


@router.put("/notifications")
async def update_notification_preferences(preferences: NotificationPreferences, authorization: Optional[str] = Header(None)):
    """
    Update notification preferences
    """
    return await SettingsController.update_notification_preferences(preferences, authorization)


@router.post("/change-password")
async def change_password(password_data: PasswordChange, authorization: Optional[str] = Header(None)):
    """
    Change user password
    """
    return await SettingsController.change_password(password_data, authorization)


@router.get("/sessions")
async def get_active_sessions(authorization: Optional[str] = Header(None)):
    """
    Get active sessions
    """
    return await SettingsController.get_active_sessions(authorization)


@router.post("/logout-session")
async def logout_session(session_id: int, authorization: Optional[str] = Header(None)):
    """
    Logout a specific session
    """
    return await SettingsController.logout_session(session_id, authorization)


@router.post("/logout-all-sessions")
async def logout_all_sessions(authorization: Optional[str] = Header(None)):
    """
    Logout all other sessions
    """
    return await SettingsController.logout_all_sessions(authorization)
