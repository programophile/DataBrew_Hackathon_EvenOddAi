"""
Sales Controller
Handles HTTP requests for sales-related endpoints
"""
from typing import Dict
from ..services.sales_service import SalesService


class SalesController:
    """Controller for sales endpoints"""

    @staticmethod
    def get_forecast(engine, sarima_model, days: int = 7) -> Dict:
        """Handle forecast request"""
        return SalesService.get_forecast(engine, days, sarima_model)

    @staticmethod
    def get_sales_data(engine, period: str = "month") -> Dict:
        """Handle sales data request"""
        return SalesService.get_sales_data(engine, period)

    @staticmethod
    def get_dashboard_metrics(engine) -> Dict:
        """Handle dashboard metrics request"""
        return SalesService.get_dashboard_metrics(engine)

    @staticmethod
    def get_best_selling(engine) -> Dict:
        """Handle best-selling product request"""
        return SalesService.get_best_selling(engine)
