"""
Predictive Analytics Service
Combines holiday data, weather forecast, and historical sales data 
to generate AI-powered insights using Gemini
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import re

# Import local modules
from .holiday import get_next_30_days_holidays, format_holidays_for_analysis

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    model = None
    print("Warning: GEMINI_API_KEY not found in environment variables")


def get_sales_data_last_60_days(engine) -> Dict:
    """
    Fetch and aggregate sales data for the last 60 days from database
    
    Args:
        engine: SQLAlchemy database engine
    
    Returns:
        Dictionary containing aggregated sales metrics
    """
    import pandas as pd
    
    try:
        # Query to get last 60 days of sales data
        query = """
            SELECT 
                DATE(transaction_date) as sale_date,
                DAYNAME(transaction_date) as day_of_week,
                SUM(transaction_qty * unit_price) as daily_sales,
                COUNT(DISTINCT transaction_id) as order_count,
                SUM(transaction_qty) as items_sold,
                AVG(transaction_qty * unit_price) as avg_order_value
            FROM transactions
            WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 60 DAY)
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
        
        # Get top 5 best days and worst 5 days
        best_days = df.nlargest(5, 'daily_sales')[['sale_date', 'daily_sales', 'day_of_week']].to_dict('records')
        worst_days = df.nsmallest(5, 'daily_sales')[['sale_date', 'daily_sales', 'day_of_week']].to_dict('records')
        
        # Day of week analysis
        day_analysis = df.groupby('day_of_week').agg({
            'daily_sales': 'mean',
            'order_count': 'mean'
        }).to_dict('index')
        
        # Calculate trends
        recent_30_days = df.head(30)['daily_sales'].mean()
        older_30_days = df.tail(30)['daily_sales'].mean()
        
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
        'total_sales_60_days': 510000,
        'avg_daily_sales': 8500,
        'total_orders': 3400,
        'avg_orders_per_day': 57,
        'best_days': [],
        'worst_days': [],
        'day_of_week_analysis': {},
        'trend': 'stable',
        'trend_percentage': 2.5,
        'data_points': 60
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
Sales Data (Last 60 Days):
- Total Sales: ${sales_data['total_sales_60_days']:,.2f}
- Average Daily Sales: ${sales_data['avg_daily_sales']:,.2f}
- Total Orders: {sales_data['total_orders']}
- Average Orders per Day: {sales_data['avg_orders_per_day']:.1f}
- Trend: {sales_data['trend']} ({sales_data['trend_percentage']:.1f}%)
- Data Points: {sales_data['data_points']} days

Best Performing Days:
"""
    
    for day in sales_data['best_days'][:3]:
        text += f"  - {day.get('sale_date', 'N/A')} ({day.get('day_of_week', 'N/A')}): ${day.get('daily_sales', 0):,.2f}\n"
    
    text += "\nWorst Performing Days:\n"
    for day in sales_data['worst_days'][:3]:
        text += f"  - {day.get('sale_date', 'N/A')} ({day.get('day_of_week', 'N/A')}): ${day.get('daily_sales', 0):,.2f}\n"
    
    if sales_data['day_of_week_analysis']:
        text += "\nDay of Week Performance:\n"
        for day, stats in list(sales_data['day_of_week_analysis'].items())[:7]:
            text += f"  - {day}: Avg ${stats['daily_sales']:,.2f}, {stats['order_count']:.0f} orders\n"
    
    return text


def generate_predictive_insights(
    sales_data: Dict,
    weather_data: List[Dict],
    holidays: List[Dict]
) -> Dict:
    """
    Generate AI-powered predictive insights using Gemini
    Analyzes patterns between weather, holidays, and sales
    
    Args:
        sales_data: Last 60 days sales metrics
        weather_data: Next 30 days weather forecast
        holidays: Next 30 days holidays
    
    Returns:
        Dictionary containing AI insights and predictions
    """
    if not model:
        return get_fallback_predictive_insights()
    
    try:
        # Format data for Gemini
        sales_text = format_sales_for_analysis(sales_data)
        weather_text = format_weather_for_analysis(weather_data)
        holidays_text = format_holidays_for_analysis(holidays)
        
        # Create comprehensive prompt
        prompt = f"""
You are an expert business analytics AI for a coffee shop called DataBrew. Analyze the following data to predict sales patterns, identify opportunities and risks for the next 30 days.

{sales_text}

{weather_text}

{holidays_text}

Based on this comprehensive data, provide insights in the following categories:

1. WEATHER IMPACT PREDICTIONS (3-4 insights):
   - How will upcoming weather patterns affect sales?
   - Identify specific days with heavy rain, extreme heat, or ideal weather
   - Suggest inventory adjustments based on weather (e.g., more iced drinks in hot weather)

2. HOLIDAY OPPORTUNITIES (2-3 insights):
   - Which holidays will boost sales and by how much?
   - Product recommendations for specific holidays (e.g., Valentine's special drinks)
   - Staffing recommendations for holiday periods

3. ABNORMALITIES & RISKS (2-3 insights):
   - Identify days with potential low sales due to weather or other factors
   - Days requiring special attention or preparation
   - Risk mitigation strategies

4. ACTIONABLE RECOMMENDATIONS (3-4 insights):
   - Specific actions to maximize revenue in next 30 days
   - Inventory management recommendations
   - Staffing optimization suggestions
   - Promotional campaign ideas tied to weather/holidays

Format your response as a JSON object with this structure:
{{
  "weather_insights": [
    {{
      "date": "2024-12-XX",
      "impact": "positive" | "negative" | "neutral",
      "prediction": "Specific prediction with numbers",
      "recommendation": "Actionable recommendation",
      "confidence": "high" | "medium" | "low"
    }}
  ],
  "holiday_insights": [
    {{
      "holiday_name": "Name",
      "date": "2024-12-XX",
      "expected_sales_increase": "percentage or amount",
      "recommendation": "Specific action to take",
      "product_suggestions": ["product1", "product2"]
    }}
  ],
  "abnormalities": [
    {{
      "date": "2024-12-XX",
      "type": "risk" | "opportunity",
      "description": "What's unusual or noteworthy",
      "impact": "Expected impact on sales",
      "mitigation": "How to handle it"
    }}
  ],
  "actionable_recommendations": [
    {{
      "category": "inventory" | "staffing" | "marketing" | "operations",
      "priority": "high" | "medium" | "low",
      "recommendation": "Specific action",
      "expected_outcome": "Expected result",
      "timeframe": "When to implement"
    }}
  ],
  "summary": {{
    "overall_outlook": "positive" | "neutral" | "challenging",
    "total_predicted_impact": "percentage change vs average",
    "key_dates_to_watch": ["date1", "date2", "date3"],
    "top_3_priorities": ["priority1", "priority2", "priority3"]
  }}
}}

Important:
- Be specific with dates, numbers, and percentages
- Base predictions on actual historical patterns from sales data
- Consider weather-sales correlations (rain = less foot traffic, hot days = more iced drinks)
- Factor in holiday impacts (Valentine's = romantic drinks, heavy rain day = low traffic)
- Provide actionable, implementable recommendations
- Return ONLY valid JSON, no markdown or additional text
"""

        # Generate insights using Gemini
        response = model.generate_content(prompt)
        insights_text = response.text.strip()
        
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
    Get weather forecast for next 30 days
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
    end_date = start_date + timedelta(days=30)
    
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
    
    for i in range(30):
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
        return "No weather forecast data available."
    
    text = f"Weather Forecast (Next 30 Days, {len(weather_data)} days):\n\n"
    
    # Identify key weather patterns
    rainy_days = [d for d in weather_data if d['precipitation'] > 5 or d['precipitation_probability'] > 60]
    hot_days = [d for d in weather_data if d['temp_max'] > 35]
    cold_days = [d for d in weather_data if d['temp_max'] < 15]
    
    text += f"Summary:\n"
    text += f"- Rainy days: {len(rainy_days)}\n"
    text += f"- Hot days (>35°C): {len(hot_days)}\n"
    text += f"- Cool days (<15°C): {len(cold_days)}\n\n"
    
    # Highlight significant weather events
    if rainy_days:
        text += "Significant Rain Expected:\n"
        for day in rainy_days[:5]:  # Show first 5 rainy days
            text += f"  - {day['date']}: {day['conditions']}, {day['precipitation']}mm rain, {day['precipitation_probability']}% chance\n"
        text += "\n"
    
    if hot_days:
        text += "Hot Days Expected:\n"
        for day in hot_days[:5]:
            text += f"  - {day['date']}: {day['temp_max']}°C max, {day['conditions']}\n"
        text += "\n"
    
    # Show next 7 days in detail
    text += "Next 7 Days Detail:\n"
    for day in weather_data[:7]:
        text += f"  - {day['date']}: {day['conditions']}, {day['temp_max']}/{day['temp_min']}°C, "
        text += f"Humidity {day['humidity']}%, Precip {day['precipitation']}mm\n"
    
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
