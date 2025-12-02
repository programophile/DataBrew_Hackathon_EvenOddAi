"""
Analytics Routes
Defines API endpoints for analytics and reporting
"""
from fastapi import APIRouter, Depends
from typing import Dict

from ..controllers.analytics_controller import AnalyticsController

router = APIRouter(prefix="", tags=["Analytics"])


def get_dependencies():
    """Dependency injection for engine"""
    from ..config.database import get_engine
    return {"engine": get_engine()}


@router.get("/inventory-predictions")
def get_inventory_predictions(deps: Dict = Depends(get_dependencies)):
    """
    Returns inventory with AI-predicted demand
    """
    return AnalyticsController.get_inventory_predictions(deps["engine"])


@router.get("/barista-schedule")
def get_barista_schedule(deps: Dict = Depends(get_dependencies)):
    """
    Returns barista schedule for today
    """
    return AnalyticsController.get_barista_schedule(deps["engine"])


@router.get("/customer-feedback")
def get_customer_feedback():
    """
    Returns recent customer feedback (mock data for now)
    """
    return AnalyticsController.get_customer_feedback()


@router.get("/sales-analytics")
def get_sales_analytics(period: str = "today", deps: Dict = Depends(get_dependencies)):
    """
    Returns aggregated sales analytics data for the analytics page
    Supports: today, yesterday, week, month
    """
    return AnalyticsController.get_sales_analytics(deps["engine"], period)


@router.get("/cash-flow")
def get_cash_flow(period: str = "month", deps: Dict = Depends(get_dependencies)):
    """
    Returns cash flow data (income vs expenses)
    """
    return AnalyticsController.get_cash_flow(deps["engine"], period)
