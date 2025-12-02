"""
Example Usage: Predictive Analytics Service
Demonstrates how to use the predictive analytics service programmatically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.holiday import get_next_30_days_holidays
from app.predictive_analytics import (
    get_weather_forecast_data,
    get_fallback_sales_data,
    generate_predictive_insights
)
import json
from datetime import datetime


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def example_1_basic_usage():
    """Example 1: Basic usage - Get all insights"""
    print_section("EXAMPLE 1: Get Complete Predictive Insights")
    
    # Step 1: Fetch holidays
    print("📅 Fetching holidays for next 30 days...")
    holidays = get_next_30_days_holidays()
    print(f"   Found {len(holidays)} holidays")
    
    # Step 2: Fetch weather
    print("\n🌤️  Fetching weather forecast for next 30 days...")
    weather = get_weather_forecast_data()
    print(f"   Got {len(weather)} days of forecast")
    
    # Step 3: Get sales data (using fallback for demo)
    print("\n💰 Getting sales data for last 60 days...")
    sales = get_fallback_sales_data()
    print(f"   Analyzed {sales['data_points']} days")
    print(f"   Average daily sales: ${sales['avg_daily_sales']:,.2f}")
    print(f"   Trend: {sales['trend']} ({sales['trend_percentage']:+.1f}%)")
    
    # Step 4: Generate AI insights
    print("\n🤖 Generating AI-powered insights with Gemini...")
    insights = generate_predictive_insights(sales, weather, holidays)
    
    print("\n✅ Insights generated successfully!")
    print(f"   Generated at: {insights['generated_at']}")
    
    return insights


def example_2_weather_analysis(insights):
    """Example 2: Analyze weather impact"""
    print_section("EXAMPLE 2: Weather Impact Analysis")
    
    weather_insights = insights.get('weather_insights', [])
    
    if not weather_insights:
        print("No weather insights available")
        return
    
    print(f"Found {len(weather_insights)} weather-related insights:\n")
    
    for i, insight in enumerate(weather_insights, 1):
        print(f"{i}. Date: {insight.get('date', 'N/A')}")
        print(f"   Impact: {insight.get('impact', 'N/A').upper()}")
        print(f"   Prediction: {insight.get('prediction', 'N/A')}")
        print(f"   Recommendation: {insight.get('recommendation', 'N/A')}")
        print(f"   Confidence: {insight.get('confidence', 'N/A')}")
        print()


def example_3_holiday_opportunities(insights):
    """Example 3: Identify holiday opportunities"""
    print_section("EXAMPLE 3: Holiday Sales Opportunities")
    
    holiday_insights = insights.get('holiday_insights', [])
    
    if not holiday_insights:
        print("No holiday insights available")
        return
    
    print(f"Found {len(holiday_insights)} holiday opportunities:\n")
    
    for i, insight in enumerate(holiday_insights, 1):
        print(f"{i}. Holiday: {insight.get('holiday_name', 'N/A')}")
        print(f"   Date: {insight.get('date', 'N/A')}")
        print(f"   Expected increase: {insight.get('expected_sales_increase', 'N/A')}")
        print(f"   Recommendation: {insight.get('recommendation', 'N/A')}")
        
        products = insight.get('product_suggestions', [])
        if products:
            print(f"   Suggested products: {', '.join(products)}")
        print()


def example_4_risk_detection(insights):
    """Example 4: Detect abnormalities and risks"""
    print_section("EXAMPLE 4: Abnormality & Risk Detection")
    
    abnormalities = insights.get('abnormalities', [])
    
    if not abnormalities:
        print("No abnormalities detected")
        return
    
    print(f"Found {len(abnormalities)} potential issues:\n")
    
    risks = [a for a in abnormalities if a.get('type') == 'risk']
    opportunities = [a for a in abnormalities if a.get('type') == 'opportunity']
    
    if risks:
        print("⚠️  RISKS:")
        for i, risk in enumerate(risks, 1):
            print(f"\n{i}. Date: {risk.get('date', 'N/A')}")
            print(f"   Description: {risk.get('description', 'N/A')}")
            print(f"   Impact: {risk.get('impact', 'N/A')}")
            print(f"   Mitigation: {risk.get('mitigation', 'N/A')}")
    
    if opportunities:
        print("\n\n✨ OPPORTUNITIES:")
        for i, opp in enumerate(opportunities, 1):
            print(f"\n{i}. Date: {opp.get('date', 'N/A')}")
            print(f"   Description: {opp.get('description', 'N/A')}")
            print(f"   Impact: {opp.get('impact', 'N/A')}")


def example_5_actionable_recommendations(insights):
    """Example 5: Get actionable recommendations"""
    print_section("EXAMPLE 5: Actionable Recommendations")
    
    recommendations = insights.get('actionable_recommendations', [])
    
    if not recommendations:
        print("No recommendations available")
        return
    
    # Group by priority
    high_priority = [r for r in recommendations if r.get('priority') == 'high']
    medium_priority = [r for r in recommendations if r.get('priority') == 'medium']
    low_priority = [r for r in recommendations if r.get('priority') == 'low']
    
    if high_priority:
        print("🔴 HIGH PRIORITY:\n")
        for i, rec in enumerate(high_priority, 1):
            print(f"{i}. [{rec.get('category', 'N/A').upper()}]")
            print(f"   Action: {rec.get('recommendation', 'N/A')}")
            print(f"   Expected outcome: {rec.get('expected_outcome', 'N/A')}")
            print(f"   Timeframe: {rec.get('timeframe', 'N/A')}")
            print()
    
    if medium_priority:
        print("\n🟡 MEDIUM PRIORITY:\n")
        for i, rec in enumerate(medium_priority, 1):
            print(f"{i}. [{rec.get('category', 'N/A').upper()}] {rec.get('recommendation', 'N/A')}")
    
    if low_priority:
        print("\n🟢 LOW PRIORITY:\n")
        for i, rec in enumerate(low_priority, 1):
            print(f"{i}. [{rec.get('category', 'N/A').upper()}] {rec.get('recommendation', 'N/A')}")


def example_6_executive_summary(insights):
    """Example 6: Executive summary"""
    print_section("EXAMPLE 6: Executive Summary")
    
    summary = insights.get('summary', {})
    
    if not summary:
        print("No summary available")
        return
    
    print("📊 BUSINESS OUTLOOK FOR NEXT 30 DAYS\n")
    
    outlook = summary.get('overall_outlook', 'N/A')
    outlook_emoji = "📈" if outlook == "positive" else "📉" if outlook == "challenging" else "➡️"
    
    print(f"{outlook_emoji}  Overall Outlook: {outlook.upper()}")
    print(f"💵 Predicted Impact: {summary.get('total_predicted_impact', 'N/A')} vs. baseline")
    
    key_dates = summary.get('key_dates_to_watch', [])
    if key_dates:
        print(f"\n📅 Key Dates to Monitor:")
        for date in key_dates:
            print(f"   • {date}")
    
    priorities = summary.get('top_3_priorities', [])
    if priorities:
        print(f"\n⭐ Top 3 Priorities:")
        for i, priority in enumerate(priorities, 1):
            print(f"   {i}. {priority}")


def example_7_export_to_json(insights):
    """Example 7: Export insights to JSON file"""
    print_section("EXAMPLE 7: Export Insights to JSON")
    
    filename = f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Insights exported to: {filepath}")
    print(f"   File size: {os.path.getsize(filepath):,} bytes")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("  PREDICTIVE ANALYTICS SERVICE - USAGE EXAMPLES")
    print("="*70)
    
    try:
        # Example 1: Get all insights
        insights = example_1_basic_usage()
        
        # Example 2: Weather analysis
        example_2_weather_analysis(insights)
        
        # Example 3: Holiday opportunities
        example_3_holiday_opportunities(insights)
        
        # Example 4: Risk detection
        example_4_risk_detection(insights)
        
        # Example 5: Actionable recommendations
        example_5_actionable_recommendations(insights)
        
        # Example 6: Executive summary
        example_6_executive_summary(insights)
        
        # Example 7: Export to JSON
        example_7_export_to_json(insights)
        
        print_section("ALL EXAMPLES COMPLETED SUCCESSFULLY! 🎉")
        print("You can now integrate these patterns into your application.\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
