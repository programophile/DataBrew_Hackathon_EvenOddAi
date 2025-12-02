import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None
    print("Warning: GEMINI_API_KEY not found in environment variables")


def generate_ai_insights(sales_data: dict) -> dict:
    """
    Generate AI insights using Gemini API based on sales data

    Args:
        sales_data: Dictionary containing sales information, trends, and patterns

    Returns:
        Dictionary containing insights list and source_data for transparency
    """
    if not model:
        return get_fallback_insights()

    try:
        # Prepare the prompt with sales data context
        low_stock_text = ", ".join(sales_data.get('low_stock_items', [])[:3]) if sales_data.get('low_stock_items') else "None"
        peak_hours_text = ", ".join(sales_data.get('peak_hours', ['Unknown'])[:3])

        prompt = f"""
You are an AI analytics assistant for a coffee shop called DataBrew. Analyze the following sales data and provide 3-4 actionable business insights.

Sales Data Summary:
- Recent sales trend: {sales_data.get('trend', 'steady')}
- Week-over-week change: {sales_data.get('wow_change', 0):.1f}%
- Top selling products: {', '.join(sales_data.get('top_products', ['Unknown'])[:3])}
- Top product revenue: ${sales_data.get('top_product_revenue', 0):.2f}
- Peak hours: {peak_hours_text}
- Peak hour customers: {sales_data.get('peak_hour_customers', 0)}
- Average daily sales: ${sales_data.get('avg_daily_sales', 0):.2f}
- Recent daily sales: ${sales_data.get('recent_daily_sales', 0):.2f}
- Average order value: ${sales_data.get('avg_order_value', 0):.2f}
- Low stock items: {low_stock_text}
- Customer count: {sales_data.get('total_customers_today', 0)}

Generate EXACTLY 3-4 insights in the following JSON format. Each insight should be actionable and specific:

[
  {{
    "type": "trending_up" | "users" | "clock" | "alert",
    "text": "Brief, actionable insight (max 100 characters)",
    "color": "#22c55e" (green for positive) | "#f59e0b" (orange for warning) | "#ef4444" (red for urgent) | "#8b5e3c" (brown for neutral)
  }}
]

Rules:
1. Provide specific numbers and percentages when possible from the data above
2. Focus on actionable recommendations (staffing, inventory, promotions, customer engagement)
3. Keep each insight under 100 characters
4. Use appropriate icon types: "trending_up" for sales trends, "users" for staffing, "clock" for time-based insights, "alert" for urgent inventory/operational matters
5. If there are low stock items, include at least one inventory alert
6. Return ONLY valid JSON, no additional text or markdown
7. Make insights specific to the data provided - use actual product names and numbers

Example:
[
  {{"type": "trending_up", "text": "Iced Latte sales up 12% WoW - stock up on milk and ice for peak hours", "color": "#22c55e"}},
  {{"type": "users", "text": "Need 2 extra baristas during 6-8 PM rush based on traffic pattern", "color": "#f59e0b"}},
  {{"type": "clock", "text": "Peak customer traffic at 3:00 PM - prepare popular items in advance", "color": "#8b5e3c"}},
  {{"type": "alert", "text": "Cappuccino beans running low - reorder immediately to avoid stockout", "color": "#ef4444"}}
]
"""

        # Generate insights using Gemini
        response = model.generate_content(prompt)
        insights_text = response.text.strip()

        # Extract JSON from the response
        # Sometimes Gemini wraps JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', insights_text, re.DOTALL)
        if json_match:
            insights_text = json_match.group(1)

        # Parse JSON
        insights = json.loads(insights_text)

        # Validate and filter insights
        valid_insights = []
        for insight in insights:
            if isinstance(insight, dict) and 'type' in insight and 'text' in insight and 'color' in insight:
                valid_insights.append(insight)

        if len(valid_insights) >= 2:
            return {
                "insights": valid_insights[:4],  # Return max 4 insights
                "source_data": sales_data
            }
        else:
            raise ValueError("Generated insights did not meet minimum requirements")

    except Exception as e:
        print(f"Error generating Gemini insights: {str(e)}")
        print(f"Response: {insights_text if 'insights_text' in locals() else 'No response'}")
        return {
            "insights": get_fallback_insights(),
            "source_data": sales_data
        }


def get_fallback_insights() -> list:
    """
    Return fallback insights when Gemini API is unavailable or fails
    """
    return [
        {
            "type": "trending_up",
            "text": "Sales analytics in progress. Check back soon for insights.",
            "color": "#22c55e"
        },
        {
            "type": "users",
            "text": "Staff scheduling optimization available soon.",
            "color": "#f59e0b"
        },
        {
            "type": "clock",
            "text": "Peak hour analysis will be displayed here.",
            "color": "#8b5e3c"
        }
    ]


def prepare_sales_summary(df) -> dict:
    """
    Prepare a sales data summary for Gemini analysis

    Args:
        df: Pandas DataFrame with sales data

    Returns:
        Dictionary with summarized sales information
    """
    import pandas as pd
    from datetime import datetime, timedelta

    summary = {}

    try:
        # Calculate basic metrics
        if not df.empty and 'sales_amount' in df.columns:
            # Average daily sales
            summary['avg_daily_sales'] = df['sales_amount'].mean()

            # Calculate trend
            recent_sales = df.tail(7)['sales_amount'].mean()
            older_sales = df.head(7)['sales_amount'].mean()
            if older_sales > 0:
                trend_pct = ((recent_sales - older_sales) / older_sales) * 100
                summary['trend'] = 'increasing' if trend_pct > 5 else 'decreasing' if trend_pct < -5 else 'steady'
                summary['wow_change'] = trend_pct
            else:
                summary['trend'] = 'steady'
                summary['wow_change'] = 0
        else:
            summary['avg_daily_sales'] = 0
            summary['trend'] = 'steady'
            summary['wow_change'] = 0

        # Top products
        if 'product_detail' in df.columns and 'transaction_qty' in df.columns:
            top_products = df.groupby('product_detail')['transaction_qty'].sum().nlargest(3).index.tolist()
            summary['top_products'] = top_products
        else:
            summary['top_products'] = ['Coffee', 'Latte', 'Espresso']

        # Peak hours
        if 'transaction_time' in df.columns:
            df['hour'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S', errors='coerce').dt.hour
            if 'hour' in df.columns and df['hour'].notna().sum() > 0:
                peak_hour = df.groupby('hour')['transaction_qty'].sum().idxmax()
                summary['peak_hours'] = f"{peak_hour}:00"
            else:
                summary['peak_hours'] = "2:00 PM - 4:00 PM"
        else:
            summary['peak_hours'] = "2:00 PM - 4:00 PM"

        # Customer trend
        summary['customer_trend'] = 'growing'

    except Exception as e:
        print(f"Error preparing sales summary: {str(e)}")
        # Return default values
        summary = {
            'avg_daily_sales': 8500,
            'trend': 'steady',
            'wow_change': 5.2,
            'top_products': ['Iced Latte', 'Cappuccino', 'Espresso'],
            'peak_hours': '2:00 PM - 4:00 PM',
            'customer_trend': 'growing'
        }

    return summary
