import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import re
from groq import Groq

# Import local modules
from .holiday import get_next_30_days_holidays, format_holidays_for_analysis

# Load environment variables
load_dotenv()

# Configure Groq API
GROQ_API_KEY = os.getenv("GROG_API_KEY")
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
    print("✓ Groq API configured successfully")
else:
    groq_client = None
    print("Warning: GROG_API_KEY not found in environment variables")


def get_sales_data_last_60_days(engine) -> Dict:
    """
    Fetch and aggregate sales data for the last 7 days from database
    
    Args:
        engine: SQLAlchemy database engine
    
    Returns:
        Dictionary containing aggregated sales metrics
    """
    import pandas as pd
    
    try:
        # Query to get last 7 days of sales data
        query = """
            SELECT 
                DATE(transaction_date) as sale_date,
                DAYNAME(transaction_date) as day_of_week,
                SUM(transaction_qty * unit_price) as daily_sales,
                COUNT(DISTINCT transaction_id) as order_count,
                SUM(transaction_qty) as items_sold,
                AVG(transaction_qty * unit_price) as avg_order_value
            FROM transactions
            WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(transaction_date), DAYNAME(transaction_date)
            ORDER BY sale_date DESC
        """
        
        df = pd.read_sql(query, engine)
        
        if df.empty:
            return get_fallback_sales_data()
        
        # Calculate metrics
        total_sales = float(df['daily_sales'].sum())
        avg_daily_sales = float(df['daily_sales'].mean())
        total_orders = int(df['order_count'].sum())
        avg_orders_per_day = float(df['order_count'].mean())
        
        # Get top 2 best days and worst 2 days
        best_days = df.nlargest(2, 'daily_sales')[['sale_date', 'daily_sales', 'day_of_week']].to_dict('records')
        worst_days = df.nsmallest(2, 'daily_sales')[['sale_date', 'daily_sales', 'day_of_week']].to_dict('records')
        
        # Day of week analysis
        day_analysis = df.groupby('day_of_week').agg({
            'daily_sales': 'mean',
            'order_count': 'mean'
        }).to_dict('index')
        
        # Calculate trends
        recent_30_days = df.head(3)['daily_sales'].mean()
        older_30_days = df.tail(3)['daily_sales'].mean()
        
        trend = "increasing" if recent_30_days > older_30_days * 1.05 else \
                "decreasing" if recent_30_days < older_30_days * 0.95 else "stable"
        trend_percentage = ((recent_30_days - older_30_days) / older_30_days * 100) if older_30_days > 0 else 0
        
        return {
            'total_sales_60_days': total_sales,
            'avg_daily_sales': avg_daily_sales,
            'total_orders': total_orders,
            'avg_orders_per_day': avg_orders_per_day,
            'best_days': best_days,
            'worst_days': worst_days,
            'day_of_week_analysis': day_analysis,
            'trend': trend,
            'trend_percentage': trend_percentage,
            'data_points': len(df)
        }
        
    except Exception as e:
        print(f"Error fetching sales data: {e}")
        return get_fallback_sales_data()


def get_fallback_sales_data() -> Dict:
    """Returns fallback sales data when database is unavailable"""
    return {
        'total_sales_60_days': 59500,
        'avg_daily_sales': 8500,
        'total_orders': 400,
        'avg_orders_per_day': 57,
        'best_days': [],
        'worst_days': [],
        'day_of_week_analysis': {},
        'trend': 'stable',
        'trend_percentage': 2.5,
        'data_points': 7
    }


def format_sales_for_analysis(sales_data: Dict) -> str:
    """
    Format sales data into a readable string for AI analysis
    
    Args:
        sales_data: Dictionary containing sales metrics
    
    Returns:
        Formatted string describing sales patterns
    """
    text = f"""
Sales (Last 7 Days): Avg ${sales_data['avg_daily_sales']:,.0f}/day, Trend: {sales_data['trend']} ({sales_data['trend_percentage']:.1f}%)
"""
    
    return text


def generate_predictive_insights(
    sales_data: Dict,
    weather_data: List[Dict],
    holidays: List[Dict]
) -> Dict:
    """
    Generate AI-powered predictive insights using Groq
    Analyzes patterns between weather, holidays, and sales
    
    Args:
        sales_data: Last 60 days sales metrics
        weather_data: Next 30 days weather forecast
        holidays: Next 30 days holidays
    
    Returns:
        Dictionary containing AI insights and predictions
    """
    if not groq_client:
        return get_fallback_predictive_insights()
    
    try:
        # Format data for Gemini
        sales_text = format_sales_for_analysis(sales_data)
        weather_text = format_weather_for_analysis(weather_data)
        holidays_text = format_holidays_for_analysis(holidays)
        
        # Create manager-focused prompt
        prompt = f"""
You are a business advisor for DataBrew Coffee Shop manager. Analyze this data and provide actionable insights:

{sales_text}
{weather_text}
{holidays_text}

Provide practical, specific JSON insights. IMPORTANT: Match this exact format:

{{
"weather_insights": [
  {{"date": "YYYY-MM-DD", "impact": "positive", "prediction": "Clear description of weather and expected effect", "recommendation": "Specific action to take", "confidence": "high/medium/low"}}
],
"holiday_insights": [
  {{"holiday_name": "Holiday Name", "date": "YYYY-MM-DD", "expected_sales_increase": "+X%", "recommendation": "Specific promotional action", "product_suggestions": ["Product A", "Product B"]}}
],
"abnormalities": [
  {{"date": "YYYY-MM-DD", "type": "risk", "description": "What might go wrong or opportunity", "impact": "Specific $ or % impact", "mitigation": "How to handle it"}}
],
"actionable_recommendations": [
  {{"category": "inventory/staffing/marketing", "priority": "high", "recommendation": "Clear action item", "expected_outcome": "Result in $ or %", "timeframe": "When to do it"}}
],
"summary": {{"overall_outlook": "positive", "total_predicted_impact": "+X%", "key_dates_to_watch": ["YYYY-MM-DD", "YYYY-MM-DD"], "top_3_priorities": ["Priority 1", "Priority 2", "Priority 3"]}}
}}

Rules:
- impact MUST be "positive", "negative", or "neutral" (not descriptions)
- type MUST be "risk" or "opportunity"
- priority MUST be "high", "medium", or "low"
- overall_outlook MUST be "positive", "neutral", or "challenging"
- Include date field in ALL abnormalities
- Max 3 items per array
"""

        # Generate insights using Groq
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert business analytics AI. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=1500
        )
        insights_text = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        json_match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', insights_text, re.DOTALL)
        if json_match:
            insights_text = json_match.group(1)
        
        # Parse JSON
        insights = json.loads(insights_text)
        
        # Add metadata
        insights['generated_at'] = datetime.now().isoformat()
        insights['data_sources'] = {
            'sales_days': sales_data['data_points'],
            'weather_days': len(weather_data),
            'holidays_count': len(holidays)
        }
        
        return insights
        
    except Exception as e:
        print(f"Error generating predictive insights: {e}")
        print(f"Response: {insights_text if 'insights_text' in locals() else 'No response'}")
        return get_fallback_predictive_insights()


def get_fallback_predictive_insights() -> Dict:
    """Returns fallback insights when AI generation fails"""
    return {
        "weather_insights": [
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "impact": "neutral",
                "prediction": "Weather data analysis in progress",
                "recommendation": "Monitor weather patterns for next update",
                "confidence": "low"
            }
        ],
        "holiday_insights": [
            {
                "holiday_name": "Analysis Pending",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "expected_sales_increase": "TBD",
                "recommendation": "Check back for holiday analysis",
                "product_suggestions": []
            }
        ],
        "abnormalities": [
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "type": "opportunity",
                "description": "Predictive analysis loading",
                "impact": "Analysis in progress",
                "mitigation": "Regular monitoring recommended"
            }
        ],
        "actionable_recommendations": [
            {
                "category": "operations",
                "priority": "medium",
                "recommendation": "Continue standard operations while analysis completes",
                "expected_outcome": "Maintain current performance",
                "timeframe": "Ongoing"
            }
        ],
        "summary": {
            "overall_outlook": "neutral",
            "total_predicted_impact": "0%",
            "key_dates_to_watch": [],
            "top_3_priorities": [
                "Wait for complete data analysis",
                "Monitor daily metrics",
                "Prepare for upcoming updates"
            ]
        },
        "generated_at": datetime.now().isoformat(),
        "data_sources": {
            "sales_days": 0,
            "weather_days": 0,
            "holidays_count": 0
        }
    }


def get_weather_forecast_data() -> List[Dict]:
    """
    Get weather forecast for next 7 days
    Wraps the weather_forcast.py functionality
    
    Returns:
        List of weather forecast dictionaries
    """
    import requests
    from datetime import datetime, timedelta
    
    # Configuration
    API_KEY = "9CP63WBQHDQ2A52ESSE85KWY4"
    latitude = 23.7918
    longitude = 90.3943
    
    start_date = datetime.today().date()
    end_date = start_date + timedelta(days=7)
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{latitude},{longitude}/{start_str}/{end_str}"
        f"?unitGroup=metric&key={API_KEY}&contentType=json&include=days"
    )
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"Weather API error: {response.status_code}")
            return get_fallback_weather_data()
        
        data = response.json()
        forecast_days = data.get("days", [])
        
        # Format weather data
        weather_list = []
        for day in forecast_days:
            weather_list.append({
                'date': day['datetime'],
                'conditions': day.get('conditions', 'Unknown'),
                'temp_max': day.get('tempmax', 0),
                'temp_min': day.get('tempmin', 0),
                'humidity': day.get('humidity', 0),
                'wind_speed': day.get('windspeed', 0),
                'precipitation': day.get('precip', 0),
                'precipitation_probability': day.get('precipprob', 0),
                'description': day.get('description', '')
            })
        
        return weather_list
        
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return get_fallback_weather_data()


def get_fallback_weather_data() -> List[Dict]:
    """Returns fallback weather data"""
    current_date = datetime.now().date()
    weather_list = []
    
    for i in range(7):
        date = current_date + timedelta(days=i)
        weather_list.append({
            'date': date.strftime('%Y-%m-%d'),
            'conditions': 'Partly cloudy',
            'temp_max': 30,
            'temp_min': 22,
            'humidity': 65,
            'wind_speed': 15,
            'precipitation': 0,
            'precipitation_probability': 20,
            'description': 'Weather data unavailable'
        })
    
    return weather_list


def format_weather_for_analysis(weather_data: List[Dict]) -> str:
    """
    Format weather forecast into a readable string for AI analysis
    
    Args:
        weather_data: List of weather forecast dictionaries
    
    Returns:
        Formatted string describing weather patterns
    """
    if not weather_data:
        return "No weather data."
    
    # Simplified format
    rainy_days = sum(1 for d in weather_data if d['precipitation'] > 5)
    hot_days = sum(1 for d in weather_data if d['temp_max'] > 35)
    
    text = f"Weather (7 days): {rainy_days} rainy, {hot_days} hot days\n"
    
    # Show first 3 days only
    for day in weather_data[:3]:
        text += f"{day['date']}: {day['conditions']}, {day['temp_max']}°C, {day['precipitation']}mm\n"
    
    return text


if __name__ == "__main__":
    # Test the predictive analytics service
    print("Testing Predictive Analytics Service...\n")
    
    print("1. Fetching holidays...")
    holidays = get_next_30_days_holidays()
    print(f"   Found {len(holidays)} holidays")
    
    print("\n2. Fetching weather forecast...")
    weather = get_weather_forecast_data()
    print(f"   Got {len(weather)} days of forecast")
    
    print("\n3. Using mock sales data...")
    sales = get_fallback_sales_data()
    
    print("\n4. Generating AI insights...")
    insights = generate_predictive_insights(sales, weather, holidays)
    
    print("\n" + "="*60)
    print("PREDICTIVE INSIGHTS GENERATED")
    print("="*60)
    print(json.dumps(insights, indent=2))
