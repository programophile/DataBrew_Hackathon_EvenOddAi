"""
Analytics Service
Handles analytics, inventory, and reporting operations
"""
import pandas as pd
from typing import Dict, List
from fastapi import HTTPException


class AnalyticsService:
    """Service for analytics and reporting operations"""

    @staticmethod
    def get_inventory_predictions(engine) -> Dict:
        """Get inventory with AI-predicted demand"""
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

            inventory_list = []
            for _, row in df.iterrows():
                current_stock = int(row['stock'])
                reorder_level = int(row['reorder_level'] or 0)

                predicted_demand = int(reorder_level * 1.5) if reorder_level > 0 else current_stock + 10

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
            raise HTTPException(status_code=500, detail=f"Error fetching inventory: {str(e)}")

    @staticmethod
    def get_barista_schedule(engine) -> Dict:
        """Get barista schedule for today"""
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
            raise HTTPException(status_code=500, detail=f"Error fetching schedule: {str(e)}")

    @staticmethod
    def get_customer_feedback() -> Dict:
        """Get recent customer feedback (mock data)"""
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

    @staticmethod
    def get_sales_analytics(engine, period: str = "today") -> Dict:
        """Get aggregated sales analytics data"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            if period == "yesterday":
                target_date = "DATE_SUB('2025-11-30', INTERVAL 1 DAY)"
                date_filter = f"DATE(transaction_date) = {target_date}"
            elif period == "week":
                target_date = "'2025-11-30'"
                date_filter = f"transaction_date >= DATE_SUB({target_date}, INTERVAL 7 DAY)"
            elif period == "month":
                target_date = "'2025-11-30'"
                date_filter = f"transaction_date >= DATE_SUB({target_date}, INTERVAL 30 DAY)"
            else:
                target_date = "'2025-11-30'"
                date_filter = f"DATE(transaction_date) = {target_date}"

            query_summary = f"""
                SELECT
                    SUM(transaction_qty * unit_price) as total_revenue,
                    COUNT(DISTINCT transaction_id) as total_orders,
                    SUM(transaction_qty) as total_items
                FROM transactions
                WHERE {date_filter}
            """
            summary_df = pd.read_sql(query_summary, engine)

            total_revenue = float(summary_df['total_revenue'].iloc[0] or 0)
            total_orders = int(summary_df['total_orders'].iloc[0] or 0)
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

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

            if not products_df.empty:
                total_product_sales = products_df['sales'].sum()
                products_df['percentage'] = (products_df['sales'] / total_product_sales * 100).round(0).astype(int)
                product_sales = products_df.to_dict('records')
            else:
                product_sales = []

            hourly_sales = []
            if period in ["today", "yesterday"]:
                query_hourly = f"""
                    SELECT
                        HOUR(transaction_time) as hour,
                        SUM(transaction_qty * unit_price) as sales
                    FROM transactions
                    WHERE {date_filter}
                    GROUP BY HOUR(transaction_time)
                    ORDER BY hour
                """
                hourly_df = pd.read_sql(query_hourly, engine)

                if not hourly_df.empty:
                    for _, row in hourly_df.iterrows():
                        hour = int(row['hour'])
                        time_label = f"{hour % 12 if hour % 12 != 0 else 12}{'PM' if hour >= 12 else 'AM'}"
                        hourly_sales.append({
                            "time": time_label,
                            "sales": float(row['sales'])
                        })

            query_monthly = """
                SELECT
                    DATE(transaction_date) as date,
                    SUM(transaction_qty * unit_price) as sales
                FROM transactions
                WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 30 DAY)
                GROUP BY DATE(transaction_date)
                ORDER BY date ASC
            """
            monthly_df = pd.read_sql(query_monthly, engine)

            monthly_sales = []
            if not monthly_df.empty:
                monthly_df['date'] = pd.to_datetime(monthly_df['date'])
                avg_daily_sales = monthly_df['sales'].mean()
                target_sales = avg_daily_sales * 1.1

                for _, row in monthly_df.iterrows():
                    monthly_sales.append({
                        "date": row['date'].strftime("%b %d"),
                        "sales": float(row['sales']),
                        "target": float(target_sales)
                    })

            return {
                "period": period,
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "avg_order_value": avg_order_value,
                "profit_margin": 24.5,
                "product_sales": product_sales,
                "hourly_sales": hourly_sales,
                "monthly_sales": monthly_sales
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")

    @staticmethod
    def get_cash_flow(engine, period: str = "month") -> Dict:
        """Get cash flow data (income vs expenses)"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
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
                label_format = lambda x: x[:3]
            else:
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
            raise HTTPException(status_code=500, detail=f"Error fetching cash flow: {str(e)}")
