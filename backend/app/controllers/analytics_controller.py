"""
Analytics Controller
Handles HTTP requests for analytics-related endpoints
"""
from typing import Dict
from ..services.analytics_service import AnalyticsService


class AnalyticsController:
    """Controller for analytics endpoints"""

    @staticmethod
    def get_inventory_predictions(engine) -> Dict:
        """Handle inventory predictions request"""
        return AnalyticsService.get_inventory_predictions(engine)

    @staticmethod
    def get_barista_schedule(engine) -> Dict:
        """Handle barista schedule request"""
        return AnalyticsService.get_barista_schedule(engine)

    @staticmethod
    def get_customer_feedback() -> Dict:
        """Handle customer feedback request"""
        return AnalyticsService.get_customer_feedback()

    @staticmethod
    def get_sales_analytics(engine, period: str = "today") -> Dict:
        """Handle sales analytics request"""
        return AnalyticsService.get_sales_analytics(engine, period)

    @staticmethod
    def get_cash_flow(engine, period: str = "month") -> Dict:
        """Handle cash flow request"""
        return AnalyticsService.get_cash_flow(engine, period)
