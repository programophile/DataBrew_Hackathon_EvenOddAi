"""
AI Routes
Defines API endpoints for AI-powered insights and predictions
"""
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Dict

router = APIRouter(prefix="", tags=["AI Insights"])


def get_dependencies():
    """Dependency injection for engine"""
    from ..config.database import get_engine
    return {"engine": get_engine()}


@router.get("/ai-insights")
def get_ai_insights(deps: Dict = Depends(get_dependencies)):
    """
    Returns AI-generated insights using Gemini AI based on recent sales data from SQL queries
    Also returns the source data used to generate insights for transparency
    """
    try:
        from ..services.gemini_service import generate_ai_insights
        from ..app.main import fetch_sales_data_for_insights

        sales_summary = fetch_sales_data_for_insights()
        result = generate_ai_insights(sales_summary)
        return {
            "insights": result["insights"],
            "source_data": result["source_data"]
        }

    except Exception as e:
        print(f"Error in ai-insights endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "insights": [
                {
                    "type": "trending_up",
                    "text": "Sales analytics are being processed. Check back soon.",
                    "color": "#22c55e"
                },
                {
                    "type": "clock",
                    "text": "Peak hours analysis in progress.",
                    "color": "#8b5e3c"
                }
            ]
        }


@router.post("/generate-insights")
def generate_new_insights(deps: Dict = Depends(get_dependencies)):
    """
    Generates fresh AI insights on demand using SQL queries and Gemini AI
    """
    try:
        from ..services.gemini_service import generate_ai_insights
        from ..app.main import fetch_sales_data_for_insights

        print("Generate insights endpoint called - fetching fresh data from database...")

        sales_summary = fetch_sales_data_for_insights()

        print(f"Sales summary prepared: {sales_summary}")

        result = generate_ai_insights(sales_summary)

        print(f"Generated {len(result['insights'])} insights")

        return {
            "insights": result["insights"],
            "source_data": result["source_data"],
            "generated_at": datetime.now().isoformat(),
            "data_summary": {
                "avg_daily_sales": sales_summary['avg_daily_sales'],
                "trend": sales_summary['trend'],
                "top_product": sales_summary['top_products'][0] if sales_summary['top_products'] else None
            }
        }

    except Exception as e:
        print(f"Error in generate-insights endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


@router.get("/predictive-insights")
def get_predictive_insights(deps: Dict = Depends(get_dependencies)):
    """
    Returns comprehensive AI-powered predictive insights combining:
    - Next 30 days holidays
    - Next 30 days weather forecast
    - Last 60 days sales data

    Analyzes patterns to predict abnormalities, opportunities, and risks
    """
    engine = deps["engine"]
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        from ..services.predictive_service import (
            get_next_30_days_holidays,
            get_weather_forecast_data,
            get_sales_data_last_60_days,
            generate_predictive_insights
        )

        print("Fetching predictive insights...")

        holidays = get_next_30_days_holidays()
        print(f"  - Found {len(holidays)} holidays")

        weather_data = get_weather_forecast_data()
        print(f"  - Got {len(weather_data)} days of weather forecast")

        sales_data = get_sales_data_last_60_days(engine)
        print(f"  - Analyzed {sales_data['data_points']} days of sales")

        insights = generate_predictive_insights(sales_data, weather_data, holidays)

        print("  ✓ Predictive insights generated successfully")

        return {
            "status": "success",
            "insights": insights,
            "data_summary": {
                "holidays_count": len(holidays),
                "weather_days": len(weather_data),
                "sales_days_analyzed": sales_data['data_points'],
                "avg_daily_sales": sales_data['avg_daily_sales'],
                "sales_trend": sales_data['trend']
            },
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error in predictive-insights endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating predictive insights: {str(e)}")


@router.get("/holidays")
def get_holidays(days: int = 30):
    """
    Returns upcoming holidays for the next N days
    """
    try:
        from ..services.holiday_service import get_next_30_days_holidays
        from datetime import datetime, timedelta

        holidays = get_next_30_days_holidays()

        if days != 30:
            end_date = datetime.now() + timedelta(days=days)
            holidays = [
                h for h in holidays
                if datetime.strptime(h['date'], '%Y-%m-%d') <= end_date
            ]

        return {
            "holidays": holidays,
            "count": len(holidays),
            "period_days": days
        }

    except Exception as e:
        print(f"Error in holidays endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching holidays: {str(e)}")


@router.get("/weather-forecast")
def get_weather_forecast(days: int = 30):
    """
    Returns weather forecast for the next N days
    """
    try:
        from ..services.predictive_service import get_weather_forecast_data

        weather_data = get_weather_forecast_data()
        weather_data = weather_data[:days]

        return {
            "forecast": weather_data,
            "count": len(weather_data),
            "period_days": days
        }

    except Exception as e:
        print(f"Error in weather-forecast endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching weather forecast: {str(e)}")
