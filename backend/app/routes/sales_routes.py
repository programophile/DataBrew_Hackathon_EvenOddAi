"""
Sales Routes
Defines API endpoints for sales-related operations
"""
from fastapi import APIRouter, Depends
from typing import Dict

from ..controllers.sales_controller import SalesController

router = APIRouter(prefix="", tags=["Sales"])


def get_dependencies():
    """Dependency injection for engine and model"""
    from ..config.database import get_engine
    from ..utils.model_loader import get_sarima_model

    return {
        "engine": get_engine(),
        "sarima_model": get_sarima_model()
    }


@router.get("/forecast")
def forecast(days: int = 7, deps: Dict = Depends(get_dependencies)):
    """
    Returns next N days sales forecast
    """
    return SalesController.get_forecast(deps["engine"], deps["sarima_model"], days)


@router.get("/sales-data")
def get_sales_data(period: str = "month", deps: Dict = Depends(get_dependencies)):
    """
    Returns sales trend data for charts
    Periods: today, week, month, custom
    """
    return SalesController.get_sales_data(deps["engine"], period)


@router.get("/dashboard-metrics")
def get_dashboard_metrics(deps: Dict = Depends(get_dependencies)):
    """
    Returns key metrics for dashboard cards
    """
    return SalesController.get_dashboard_metrics(deps["engine"])


@router.get("/best-selling")
def get_best_selling(deps: Dict = Depends(get_dependencies)):
    """
    Returns the best-selling product today
    """
    return SalesController.get_best_selling(deps["engine"])
