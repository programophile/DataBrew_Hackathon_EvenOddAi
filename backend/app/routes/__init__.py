"""
Routes package - API route definitions
"""
from .auth_routes import router as auth_router
from .sales_routes import router as sales_router
from .analytics_routes import router as analytics_router
from .settings_routes import router as settings_router
from .inventory_routes import router as inventory_router
from .ai_routes import router as ai_router

__all__ = [
    'auth_router',
    'sales_router',
    'analytics_router',
    'settings_router',
    'inventory_router',
    'ai_router'
]
