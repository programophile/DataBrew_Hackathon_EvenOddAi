# backend.py
from fastapi import FastAPI, HTTPException
import pandas as pd
import pickle
import os
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from .gemini_service import generate_ai_insights, prepare_sales_summary

app = FastAPI(title="Coffee Sales Analytics API")

# Fixed current date for the application (2023-06-24)
CURRENT_DATE = datetime(2023, 6, 24)

# Allow CORS for your frontend (adjust origin as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-trained SARIMA model (if exists)
sarima_model = None
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "sarima_model_forcast.pkl")
if os.path.exists(model_path):
    try:
        with open(model_path, "rb") as f:
            sarima_model = pickle.load(f)
        print("SARIMA model loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load SARIMA model: {e}")
else:
    print(f"Warning: SARIMA model not found at {model_path}")

# SQL connection setup
try:
    engine = create_engine("mysql+pymysql://root:@localhost:3306/databrew")
    print("Database connection established successfully")
except Exception as e:
    print(f"Warning: Could not create database engine: {e}")
    engine = None

@app.get("/")
def root():
    """
    Root endpoint - shows API status and available endpoints
    """
    return {
        "message": "Coffee Sales Analytics API",
        "status": "running",
        "database": "connected" if engine else "disconnected",
        "endpoints": {
            "/forecast": "GET - Returns sales forecast for next N days",
            "/ai-insights": "GET - Returns AI-generated insights",
            "/sales-data": "GET - Returns sales trend data",
            "/dashboard-metrics": "GET - Returns dashboard key metrics",
            "/best-selling": "GET - Returns best-selling product",
            "/inventory-predictions": "GET - Returns inventory demand predictions",
            "/customer-feedback": "GET - Returns recent customer feedback",
            "/barista-schedule": "GET - Returns barista schedule",
            "/docs": "API documentation"
        }
    }

@app.get("/forecast")
def forecast(days: int = 7):
    """
    Returns next N days sales forecast
    """
    print(f"Forecast endpoint called with days={days}")

    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        print("Fetching data from database...")
        # Fetch from transactions table (more structured)
        query = """
            SELECT transaction_date, transaction_qty, unit_price
            FROM transactions
            ORDER BY transaction_date DESC
            LIMIT 5000
        """
        df = pd.read_sql(query, engine)

        if df.empty:
            # Fallback to coffee_sales table if transactions is empty
            query = """
                SELECT transaction_date, transaction_qty, unit_price
                FROM coffee_sales
                ORDER BY transaction_date DESC
                LIMIT 5000
            """
            df = pd.read_sql(query, engine)

        print(f"Fetched {len(df)} rows from database")

        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['transaction_qty'] = pd.to_numeric(df['transaction_qty'], errors='coerce')
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        df['sales_amount'] = df['transaction_qty'] * df['unit_price']

        # Aggregate daily sales
        daily_sales = df.groupby('transaction_date')['sales_amount'].sum().sort_index()
        print(f"Aggregated to {len(daily_sales)} days of sales data")

        # Use pre-trained model or simple forecast
        if sarima_model is not None:
            print("Using pre-trained SARIMA model...")
            forecast_obj = sarima_model.get_forecast(steps=days)
            forecast_values = forecast_obj.predicted_mean.values.tolist()
        else:
            print("Using simple average forecast...")
            recent_avg = daily_sales.tail(7).mean()
            forecast_values = [float(recent_avg)] * days

        print(f"Forecast generated: {forecast_values[:5]}...")

        return {
            "forecast_next_days": forecast_values,
            "last_date_in_data": daily_sales.index[-1].strftime("%Y-%m-%d") if len(daily_sales) > 0 else None,
            "days_forecasted": days
        }
    except Exception as e:
        print(f"Error in forecast endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")


def fetch_sales_data_for_insights():
    """
    Helper function to fetch and process sales data for AI insights
    Returns a sales_summary dictionary
    """
    if engine is None:
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
        'low_stock_items': inventory_df['item_name'].tolist() if not inventory_df.empty else []
    }

    return sales_summary


@app.get("/ai-insights")
def get_ai_insights():
    """
    Returns AI-generated insights using Gemini AI based on recent sales data from SQL queries
    """
    try:
        sales_summary = fetch_sales_data_for_insights()
        insights = generate_ai_insights(sales_summary)
        return {"insights": insights}

    except Exception as e:
        print(f"Error in ai-insights endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return fallback insights on error
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


@app.post("/generate-insights")
def generate_new_insights():
    """
    Generates fresh AI insights on demand using SQL queries and Gemini AI
    """
    try:
        print("Generate insights endpoint called - fetching fresh data from database...")

        sales_summary = fetch_sales_data_for_insights()

        print(f"Sales summary prepared: {sales_summary}")

        # Generate fresh AI insights using Gemini with SQL-derived data
        insights = generate_ai_insights(sales_summary)

        print(f"Generated {len(insights)} insights")

        return {
            "insights": insights,
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


@app.get("/sales-data")
def get_sales_data(period: str = "month"):
    """
    Returns sales trend data for charts
    Periods: today, week, month, custom
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Determine date range based on period
        if period == "today":
            days = 1
        elif period == "week":
            days = 7
        elif period == "month":
            days = 30
        else:
            days = 30  # default

        query = """
            SELECT transaction_date, transaction_qty, unit_price
            FROM transactions
            WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL %s DAY)
            ORDER BY transaction_date ASC
        """ % days

        df = pd.read_sql(query, engine)

        if df.empty:
            # Fallback to coffee_sales
            query = """
                SELECT transaction_date, transaction_qty, unit_price
                FROM coffee_sales
                LIMIT 1000
            """
            df = pd.read_sql(query, engine)

        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
        df['transaction_qty'] = pd.to_numeric(df['transaction_qty'], errors='coerce')
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        df['sales_amount'] = df['transaction_qty'] * df['unit_price']

        # Group by date
        daily_sales = df.groupby('transaction_date')['sales_amount'].sum().reset_index()
        daily_sales = daily_sales.sort_values('transaction_date')

        # Format data for frontend
        sales_data = []
        for _, row in daily_sales.iterrows():
            sales_data.append({
                "date": row['transaction_date'].strftime("%b %d"),
                "sales": float(row['sales_amount'])
            })

        return {"sales_data": sales_data, "period": period}

    except Exception as e:
        print(f"Error in sales-data endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching sales data: {str(e)}")


@app.get("/dashboard-metrics")
def get_dashboard_metrics():
    """
    Returns key metrics for dashboard cards
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Get today's sales
        query_today = """
            SELECT SUM(transaction_qty * unit_price) as total_sales,
                   COUNT(DISTINCT transaction_id) as total_customers
            FROM transactions
            WHERE DATE(transaction_date) = '2025-11-30'
        """

        today_data = pd.read_sql(query_today, engine)

        # Get yesterday's sales for comparison
        query_yesterday = """
            SELECT SUM(transaction_qty * unit_price) as total_sales
            FROM transactions
            WHERE DATE(transaction_date) = DATE_SUB('2025-11-30', INTERVAL 1 DAY)
        """

        yesterday_data = pd.read_sql(query_yesterday, engine)

        # Calculate trend
        today_sales = float(today_data['total_sales'].iloc[0] or 0)
        yesterday_sales = float(yesterday_data['total_sales'].iloc[0] or 0)

        if yesterday_sales > 0:
            sales_trend = ((today_sales - yesterday_sales) / yesterday_sales) * 100
        else:
            sales_trend = 0

        # Get total customers
        total_customers = int(today_data['total_customers'].iloc[0] or 0)

        # Get profit margin (simplified calculation)
        profit_margin = 22  # Default

        # Get active baristas needed (from staff table)
        query_staff = """
            SELECT COUNT(*) as active_baristas
            FROM staff
            WHERE role = 'barista'
        """
        staff_data = pd.read_sql(query_staff, engine)
        active_baristas = int(staff_data['active_baristas'].iloc[0] or 3)

        # Get last 7 days for sparkline data
        query_week = """
            SELECT DATE(transaction_date) as date, SUM(transaction_qty * unit_price) as sales
            FROM transactions
            WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 7 DAY)
            GROUP BY DATE(transaction_date)
            ORDER BY date ASC
        """
        week_data = pd.read_sql(query_week, engine)

        sales_sparkline = [float(x) for x in week_data['sales'].tolist()] if not week_data.empty else [8200, 8500, 9100, 8800, 9300, 10200, 12540]

        return {
            "total_sales": today_sales,
            "sales_trend": sales_trend,
            "total_customers": total_customers,
            "profit_margin": profit_margin,
            "active_baristas": active_baristas,
            "sales_sparkline": sales_sparkline
        }

    except Exception as e:
        print(f"Error in dashboard-metrics endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")


@app.get("/best-selling")
def get_best_selling():
    """
    Returns the best-selling product today
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        query = """
            SELECT
                product_detail,
                product_type,
                SUM(transaction_qty) as units_sold,
                SUM(transaction_qty * unit_price) as revenue
            FROM transactions
            WHERE DATE(transaction_date) = '2025-11-30'
            GROUP BY product_detail, product_type
            ORDER BY units_sold DESC
            LIMIT 1
        """

        df = pd.read_sql(query, engine)

        if df.empty:
            # Fallback to coffee_sales
            query = """
                SELECT
                    product_detail,
                    product_type,
                    SUM(CAST(transaction_qty AS UNSIGNED)) as units_sold,
                    SUM(CAST(transaction_qty AS UNSIGNED) * CAST(unit_price AS DECIMAL(10,2))) as revenue
                FROM coffee_sales
                GROUP BY product_detail, product_type
                ORDER BY units_sold DESC
                LIMIT 1
            """
            df = pd.read_sql(query, engine)

        if not df.empty:
            product = df.iloc[0]

            # Get yesterday's data for comparison
            query_yesterday = """
                SELECT SUM(transaction_qty) as units_sold
                FROM transactions
                WHERE DATE(transaction_date) = DATE_SUB('2025-11-30', INTERVAL 1 DAY)
                AND product_detail = %s
            """

            yesterday_df = pd.read_sql(query_yesterday, engine, params=[product['product_detail']])
            yesterday_units = float(yesterday_df['units_sold'].iloc[0] or 0) if not yesterday_df.empty else 0

            change_pct = 0
            if yesterday_units > 0:
                change_pct = ((float(product['units_sold']) - yesterday_units) / yesterday_units) * 100

            return {
                "product_name": product['product_detail'],
                "product_type": product['product_type'],
                "units_sold": int(product['units_sold']),
                "revenue": float(product['revenue']),
                "change_percent": change_pct
            }
        else:
            return {
                "product_name": "Iced Caramel Latte",
                "product_type": "Coffee",
                "units_sold": 0,
                "revenue": 0,
                "change_percent": 0
            }

    except Exception as e:
        print(f"Error in best-selling endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching best-selling: {str(e)}")


@app.get("/inventory-predictions")
def get_inventory_predictions():
    """
    Returns inventory with AI-predicted demand
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        query = """
            SELECT
                item_name,
                stock,
                unit,
                reorder_level
            FROM inventory
            ORDER BY item_name
        """

        df = pd.read_sql(query, engine)

        if df.empty:
            return {"inventory": []}

        # Calculate predicted demand based on current stock and reorder level
        inventory_list = []
        for _, row in df.iterrows():
            current_stock = int(row['stock'])
            reorder_level = int(row['reorder_level'] or 0)

            # Simple prediction: 1.5x current consumption rate
            predicted_demand = int(reorder_level * 1.5) if reorder_level > 0 else current_stock + 10

            # Determine alert level
            if current_stock < reorder_level:
                alert_level = "critical"
                demand_level = "High Demand"
            elif current_stock < reorder_level * 1.5:
                alert_level = "warning"
                demand_level = "Medium"
            else:
                alert_level = "safe"
                demand_level = "Low"

            inventory_list.append({
                "product": row['item_name'],
                "current_stock": f"{current_stock} {row['unit']}",
                "predicted_demand": f"{predicted_demand} {row['unit']}",
                "demand_level": demand_level,
                "alert_level": alert_level
            })

        return {"inventory": inventory_list}

    except Exception as e:
        print(f"Error in inventory-predictions endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching inventory: {str(e)}")


@app.get("/barista-schedule")
def get_barista_schedule():
    """
    Returns barista schedule for today
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        query = """
            SELECT
                name,
                role,
                shift_start,
                shift_end,
                performance_score
            FROM staff
            WHERE role IN ('barista', 'Barista')
            ORDER BY shift_start
        """

        df = pd.read_sql(query, engine)

        schedule = []
        for _, row in df.iterrows():
            schedule.append({
                "name": row['name'],
                "role": row['role'],
                "shift": f"{row['shift_start']} - {row['shift_end']}",
                "performance": float(row['performance_score'] or 0)
            })

        return {"schedule": schedule}

    except Exception as e:
        print(f"Error in barista-schedule endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching schedule: {str(e)}")


@app.get("/customer-feedback")
def get_customer_feedback():
    """
    Returns recent customer feedback (mock data for now)
    """
    # This would ideally come from a feedback/reviews table
    feedback = [
        {
            "customer": "John D.",
            "rating": 5,
            "comment": "Best coffee in town! The service is excellent.",
            "date": "Today"
        },
        {
            "customer": "Sarah M.",
            "rating": 4,
            "comment": "Great ambiance, but wait time was a bit long.",
            "date": "Yesterday"
        },
        {
            "customer": "Mike R.",
            "rating": 5,
            "comment": "Amazing Iced Caramel Latte. Will come back!",
            "date": "2 days ago"
        }
    ]

    return {"feedback": feedback}


@app.get("/sales-analytics")
def get_sales_analytics():
    """
    Returns aggregated sales analytics data for the analytics page
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Get 30-day summary
        query_summary = """
            SELECT 
                SUM(transaction_qty * unit_price) as total_revenue,
                COUNT(DISTINCT transaction_id) as total_orders,
                SUM(transaction_qty) as total_items
            FROM transactions
            WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 30 DAY)
        """
        summary_df = pd.read_sql(query_summary, engine)
        
        total_revenue = float(summary_df['total_revenue'].iloc[0] or 0)
        total_orders = int(summary_df['total_orders'].iloc[0] or 0)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

        # Get product breakdown
        query_products = """
            SELECT 
                product_detail as name,
                SUM(transaction_qty * unit_price) as sales
            FROM transactions
            WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 30 DAY)
            GROUP BY product_detail
            ORDER BY sales DESC
            LIMIT 5
        """
        products_df = pd.read_sql(query_products, engine)
        
        # Calculate percentages
        if not products_df.empty:
            total_product_sales = products_df['sales'].sum()
            products_df['percentage'] = (products_df['sales'] / total_product_sales * 100).round(0).astype(int)
            product_sales = products_df.to_dict('records')
        else:
            product_sales = []

        # Get hourly breakdown for today
        query_hourly = """
            SELECT 
                HOUR(transaction_time) as hour,
                SUM(transaction_qty * unit_price) as sales
            FROM transactions
            WHERE DATE(transaction_date) = '2025-11-30'
            GROUP BY HOUR(transaction_time)
            ORDER BY hour
        """
        hourly_df = pd.read_sql(query_hourly, engine)
        
        if not hourly_df.empty:
            hourly_sales = []
            for _, row in hourly_df.iterrows():
                hour = int(row['hour'])
                time_label = f"{hour % 12 if hour % 12 != 0 else 12}{'PM' if hour >= 12 else 'AM'}"
                hourly_sales.append({
                    "time": time_label,
                    "sales": float(row['sales'])
                })
        else:
            hourly_sales = []

        # Get daily sales for last 30 days
        query_daily = """
            SELECT 
                DATE(transaction_date) as date,
                SUM(transaction_qty * unit_price) as sales
            FROM transactions
            WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 30 DAY)
            GROUP BY DATE(transaction_date)
            ORDER BY date ASC
        """
        daily_df = pd.read_sql(query_daily, engine)
        
        if not daily_df.empty:
            daily_df['date'] = pd.to_datetime(daily_df['date'])
            monthly_sales = []
            for _, row in daily_df.iterrows():
                monthly_sales.append({
                    "date": row['date'].strftime("%b %d"),
                    "sales": float(row['sales']),
                    "target": avg_order_value * 10  # Mock target
                })
        else:
            monthly_sales = []

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "avg_order_value": avg_order_value,
            "profit_margin": 24.5,  # Can be calculated if cost data available
            "product_sales": product_sales,
            "hourly_sales": hourly_sales,
            "monthly_sales": monthly_sales
        }

    except Exception as e:
        print(f"Error in sales-analytics endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")


@app.get("/cash-flow")
def get_cash_flow(period: str = "month"):
    """
    Returns cash flow data (income vs expenses)
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Determine date range and grouping based on period
        if period == "today":
            query = """
                SELECT 
                    HOUR(transaction_time) as period_label,
                    SUM(transaction_qty * unit_price) as income,
                    SUM(transaction_qty * unit_price * 0.7) as expenses
                FROM transactions
                WHERE DATE(transaction_date) = '2025-11-30'
                GROUP BY HOUR(transaction_time)
                ORDER BY period_label
            """
            label_format = lambda x: f"{int(x) % 12 if int(x) % 12 != 0 else 12}{'PM' if int(x) >= 12 else 'AM'}"
        elif period == "week":
            query = """
                SELECT 
                    DAYNAME(transaction_date) as period_label,
                    SUM(transaction_qty * unit_price) as income,
                    SUM(transaction_qty * unit_price * 0.7) as expenses
                FROM transactions
                WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 7 DAY)
                GROUP BY DATE(transaction_date), DAYNAME(transaction_date)
                ORDER BY DATE(transaction_date)
            """
            label_format = lambda x: x[:3]  # Mon, Tue, etc.
        else:  # month or custom
            query = """
                SELECT 
                    DATE_FORMAT(transaction_date, '%%b %%d') as period_label,
                    SUM(transaction_qty * unit_price) as income,
                    SUM(transaction_qty * unit_price * 0.7) as expenses
                FROM transactions
                WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 30 DAY)
                GROUP BY DATE(transaction_date)
                ORDER BY DATE(transaction_date)
            """
            label_format = lambda x: x

        df = pd.read_sql(query, engine)

        if df.empty:
            return {"cash_flow": []}

        cash_flow = []
        for _, row in df.iterrows():
            label = row['period_label']
            if period == "today":
                label = label_format(label)
            elif period == "week":
                label = label_format(label)
            
            cash_flow.append({
                "month": label,
                "income": float(row['income']),
                "expenses": float(row['expenses'])
            })

        return {"cash_flow": cash_flow, "period": period}

    except Exception as e:
        print(f"Error in cash-flow endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching cash flow: {str(e)}")
