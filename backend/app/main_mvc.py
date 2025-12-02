"""
DataBrew Coffee Sales Analytics API - MVC Architecture
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.database import init_db
from .config.settings import APP_NAME, CORS_ORIGINS
from .utils.model_loader import load_sarima_model

# Import routers
from .routes import (
    auth_router,
    sales_router,
    analytics_router,
    settings_router,
    inventory_router,
    ai_router
)

# Initialize FastAPI app
app = FastAPI(title=APP_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application resources on startup"""
    print("="*60)
    print(f"Starting {APP_NAME}")
    print("="*60)

    # Initialize database connection
    init_db()

    # Load ML models
    load_sarima_model()

    print("="*60)
    print("Application startup complete")
    print("="*60)


@app.get("/")
def root():
    """
    Root endpoint - shows API status and available endpoints
    """
    return {
        "message": "Coffee Sales Analytics API",
        "version": "2.0.0",
        "architecture": "MVC Pattern",
        "status": "running",
        "endpoints": {
            "/login": "POST - Login with admin credentials (admin@gmail.com / admin123)",
            "/signup": "POST - Signup (disabled - only admin access)",
            "/logout": "POST - Logout current session",
            "/profile": "GET - Get user profile (requires auth)",
            "/verify": "GET - Verify authentication token",
            "/forecast": "GET - Returns sales forecast for next N days",
            "/ai-insights": "GET - Returns AI-generated insights",
            "/generate-insights": "POST - Generate fresh AI insights",
            "/predictive-insights": "GET - Returns comprehensive predictive insights",
            "/holidays": "GET - Returns upcoming holidays",
            "/weather-forecast": "GET - Returns weather forecast",
            "/sales-data": "GET - Returns sales trend data",
            "/dashboard-metrics": "GET - Returns dashboard key metrics",
            "/best-selling": "GET - Returns best-selling product",
            "/inventory-predictions": "GET - Returns inventory demand predictions",
            "/customer-feedback": "GET - Returns recent customer feedback",
            "/barista-schedule": "GET - Returns barista schedule",
            "/sales-analytics": "GET - Returns aggregated sales analytics",
            "/cash-flow": "GET - Returns cash flow data",
            "/ingredients": "GET - Get all ingredients",
            "/products": "GET - Get all products",
            "/settings/profile": "GET/PUT - Get/Update user profile",
            "/settings/shop": "GET/PUT - Get/Update shop details",
            "/settings/notifications": "GET/PUT - Get/Update notification preferences",
            "/settings/change-password": "POST - Change password",
            "/settings/sessions": "GET - Get active sessions",
            "/settings/logout-session": "POST - Logout specific session",
            "/settings/logout-all-sessions": "POST - Logout all other sessions",
            "/docs": "API documentation (Swagger UI)",
            "/redoc": "API documentation (ReDoc)"
        }
    }


# Register routers
app.include_router(auth_router)
app.include_router(sales_router)
app.include_router(analytics_router)
app.include_router(settings_router)
app.include_router(inventory_router)
app.include_router(ai_router)


# Helper function for AI insights (kept for compatibility with ai_routes)
def fetch_sales_data_for_insights():
    """
    Helper function to fetch and process sales data for AI insights
    Returns a sales_summary dictionary
    """
    from .config.database import get_engine
    import pandas as pd

    engine = get_engine()
    if engine is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Database connection not available")

    # 1. Get recent sales trends with SQL
    query_trends = """
        SELECT
            DATE(transaction_date) as date,
            SUM(transaction_qty * unit_price) as daily_sales,
            COUNT(DISTINCT transaction_id) as order_count,
            SUM(transaction_qty) as items_sold
        FROM transactions
        WHERE transaction_date >= DATE_SUB('2023-06-24', INTERVAL 14 DAY)
        GROUP BY DATE(transaction_date)
        ORDER BY date DESC
    """
    trends_df = pd.read_sql(query_trends, engine)

    # 2. Get top products with SQL
    query_products = """
        SELECT
            product_detail,
            product_type,
            SUM(transaction_qty) as total_qty,
            SUM(transaction_qty * unit_price) as total_revenue,
            COUNT(DISTINCT transaction_id) as order_count
        FROM transactions
        WHERE transaction_date >= DATE_SUB('2023-06-24', INTERVAL 7 DAY)
        GROUP BY product_detail, product_type
        ORDER BY total_revenue DESC
        LIMIT 5
    """
    products_df = pd.read_sql(query_products, engine)

    # 3. Get hourly patterns with SQL
    query_hourly = """
        SELECT
            HOUR(transaction_time) as hour,
            COUNT(DISTINCT transaction_id) as customer_count,
            SUM(transaction_qty * unit_price) as hourly_sales
        FROM transactions
        WHERE DATE(transaction_date) >= DATE_SUB('2023-06-24', INTERVAL 3 DAY)
        GROUP BY HOUR(transaction_time)
        ORDER BY hourly_sales DESC
        LIMIT 3
    """
    hourly_df = pd.read_sql(query_hourly, engine)

    # 4. Get inventory levels with SQL
    query_inventory = """
        SELECT
            item_name,
            stock,
            reorder_level
        FROM inventory
        WHERE stock < reorder_level * 1.5
        ORDER BY (stock / NULLIF(reorder_level, 0)) ASC
        LIMIT 3
    """
    inventory_df = pd.read_sql(query_inventory, engine)

    # 5. Calculate week-over-week changes
    if not trends_df.empty and len(trends_df) >= 7:
        current_week_sales = trends_df.head(7)['daily_sales'].sum()
        previous_week_sales = trends_df.tail(7)['daily_sales'].sum() if len(trends_df) >= 14 else current_week_sales
        wow_change = ((current_week_sales - previous_week_sales) / previous_week_sales * 100) if previous_week_sales > 0 else 0
    else:
        wow_change = 0

    # 6. Prepare comprehensive sales summary for Gemini
    sales_summary = {
        'avg_daily_sales': float(trends_df['daily_sales'].mean()) if not trends_df.empty else 0,
        'recent_daily_sales': float(trends_df.head(1)['daily_sales'].iloc[0]) if not trends_df.empty else 0,
        'wow_change': round(wow_change, 1),
        'trend': 'increasing' if wow_change > 5 else 'decreasing' if wow_change < -5 else 'steady',
        'top_products': products_df['product_detail'].tolist() if not products_df.empty else [],
        'top_product_revenue': float(products_df['total_revenue'].iloc[0]) if not products_df.empty else 0,
        'peak_hours': [f"{int(row['hour'])}:00" for _, row in hourly_df.iterrows()] if not hourly_df.empty else [],
        'peak_hour_customers': int(hourly_df['customer_count'].max()) if not hourly_df.empty else 0,
        'total_customers_today': int(trends_df.head(1)['order_count'].iloc[0]) if not trends_df.empty else 0,
        'avg_order_value': float(current_week_sales / trends_df.head(7)['order_count'].sum()) if not trends_df.empty and trends_df.head(7)['order_count'].sum() > 0 else 0,
        'low_stock_items': inventory_df['item_name'].tolist() if not inventory_df.empty else [],
        'total_weekly_sales': float(current_week_sales) if not trends_df.empty else 0,
        'total_weekly_orders': int(trends_df.head(7)['order_count'].sum()) if not trends_df.empty else 0,
        'total_items_sold': int(trends_df.head(7)['items_sold'].sum()) if not trends_df.empty else 0,
        'best_selling_product': products_df['product_detail'].iloc[0] if not products_df.empty else None,
        'best_selling_qty': int(products_df['total_qty'].iloc[0]) if not products_df.empty else 0,
        'top_5_products': products_df[['product_detail', 'total_revenue', 'total_qty']].to_dict('records') if not products_df.empty else [],
        'daily_sales_last_7_days': trends_df.head(7)[['date', 'daily_sales', 'order_count']].to_dict('records') if not trends_df.empty else [],
        'peak_hours_details': hourly_df[['hour', 'customer_count', 'hourly_sales']].to_dict('records') if not hourly_df.empty else [],
        'inventory_alerts': inventory_df[['item_name', 'stock', 'reorder_level']].to_dict('records') if not inventory_df.empty else []
    }

    return sales_summary


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
