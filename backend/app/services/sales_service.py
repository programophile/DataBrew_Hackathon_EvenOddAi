"""
Sales Service
Handles sales data retrieval and processing
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy import text


class SalesService:
    """Service for sales-related operations"""

    @staticmethod
    def get_forecast(engine, days: int = 7, sarima_model=None) -> Dict:
        """
        Get sales forecast for next N days

        Args:
            engine: Database engine
            days: Number of days to forecast
            sarima_model: Pre-trained SARIMA model (optional)

        Returns:
            Dictionary with forecast data
        """
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            print(f"Fetching data from database for {days} days forecast...")

            query = """
                SELECT transaction_date, transaction_qty, unit_price
                FROM transactions
                ORDER BY transaction_date DESC
                LIMIT 5000
            """
            df = pd.read_sql(query, engine)

            if df.empty:
                query = """
                    SELECT transaction_date, transaction_qty, unit_price
                    FROM coffee_sales
                    ORDER BY transaction_date DESC
                    LIMIT 5000
                """
                df = pd.read_sql(query, engine)

            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
            df['transaction_qty'] = pd.to_numeric(df['transaction_qty'], errors='coerce')
            df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
            df['sales_amount'] = df['transaction_qty'] * df['unit_price']

            daily_sales = df.groupby('transaction_date')['sales_amount'].sum().sort_index()

            if sarima_model is not None:
                forecast_obj = sarima_model.get_forecast(steps=days)
                forecast_values = forecast_obj.predicted_mean.values.tolist()
            else:
                recent_avg = daily_sales.tail(7).mean()
                forecast_values = [float(recent_avg)] * days

            return {
                "forecast_next_days": forecast_values,
                "last_date_in_data": daily_sales.index[-1].strftime("%Y-%m-%d") if len(daily_sales) > 0 else None,
                "days_forecasted": days
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

    @staticmethod
    def get_sales_data(engine, period: str = "month") -> Dict:
        """
        Get sales trend data for charts

        Args:
            engine: Database engine
            period: Period (today, week, month, custom)

        Returns:
            Dictionary with sales data
        """
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            if period == "today":
                days = 1
            elif period == "week":
                days = 7
            elif period == "month":
                days = 30
            else:
                days = 30

            query = f"""
                SELECT transaction_date, transaction_qty, unit_price
                FROM transactions
                WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL {days} DAY)
                ORDER BY transaction_date ASC
            """

            df = pd.read_sql(query, engine)

            if df.empty:
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

            daily_sales = df.groupby('transaction_date')['sales_amount'].sum().reset_index()
            daily_sales = daily_sales.sort_values('transaction_date')

            sales_data = []
            for _, row in daily_sales.iterrows():
                sales_data.append({
                    "date": row['transaction_date'].strftime("%b %d"),
                    "sales": float(row['sales_amount'])
                })

            return {"sales_data": sales_data, "period": period}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching sales data: {str(e)}")

    @staticmethod
    def get_dashboard_metrics(engine) -> Dict:
        """
        Get key metrics for dashboard cards

        Args:
            engine: Database engine

        Returns:
            Dictionary with dashboard metrics
        """
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            query_today = """
                SELECT SUM(transaction_qty * unit_price) as total_sales,
                       COUNT(DISTINCT transaction_id) as total_customers
                FROM transactions
                WHERE DATE(transaction_date) = '2025-11-30'
            """
            today_data = pd.read_sql(query_today, engine)

            query_yesterday = """
                SELECT SUM(transaction_qty * unit_price) as total_sales
                FROM transactions
                WHERE DATE(transaction_date) = DATE_SUB('2025-11-30', INTERVAL 1 DAY)
            """
            yesterday_data = pd.read_sql(query_yesterday, engine)

            today_sales = float(today_data['total_sales'].iloc[0] or 0)
            yesterday_sales = float(yesterday_data['total_sales'].iloc[0] or 0)

            if yesterday_sales > 0:
                sales_trend = ((today_sales - yesterday_sales) / yesterday_sales) * 100
            else:
                sales_trend = 0

            total_customers = int(today_data['total_customers'].iloc[0] or 0)

            query_staff = """
                SELECT COUNT(*) as active_baristas
                FROM staff
                WHERE role = 'barista'
            """
            staff_data = pd.read_sql(query_staff, engine)
            active_baristas = int(staff_data['active_baristas'].iloc[0] or 3)

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
                "profit_margin": 22,
                "active_baristas": active_baristas,
                "sales_sparkline": sales_sparkline
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")

    @staticmethod
    def get_best_selling(engine) -> Dict:
        """
        Get best-selling product today

        Args:
            engine: Database engine

        Returns:
            Dictionary with best-selling product data
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

                query_yesterday = """
                    SELECT SUM(transaction_qty) as units_sold
                    FROM transactions
                    WHERE DATE(transaction_date) = DATE_SUB('2025-11-30', INTERVAL 1 DAY)
                    AND product_detail = :product_detail
                """

                yesterday_df = pd.read_sql(text(query_yesterday), engine, params={'product_detail': product['product_detail']})
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
            raise HTTPException(status_code=500, detail=f"Error fetching best-selling: {str(e)}")
