"""
Test script for Predictive Analytics Service
Tests the integration of holidays, weather, and sales data
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.holiday import get_next_30_days_holidays, format_holidays_for_analysis
from app.predictive_analytics import (
    get_weather_forecast_data,
    format_weather_for_analysis,
    get_fallback_sales_data,
    format_sales_for_analysis,
    generate_predictive_insights
)
import json


def test_holiday_service():
    """Test holiday data fetching"""
    print("="*60)
    print("TESTING HOLIDAY SERVICE")
    print("="*60)
    
    try:
        holidays = get_next_30_days_holidays()
        print(f"✓ Successfully fetched {len(holidays)} holidays")
        
        if holidays:
            print("\nSample holidays:")
            for holiday in holidays[:3]:
                print(f"  - {holiday['date']}: {holiday['name']} ({holiday['type']})")
        
        formatted = format_holidays_for_analysis(holidays)
        print(f"\n✓ Successfully formatted holidays for analysis")
        print(f"  Preview: {formatted[:200]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error testing holiday service: {e}")
        return False


def test_weather_service():
    """Test weather data fetching"""
    print("\n" + "="*60)
    print("TESTING WEATHER SERVICE")
    print("="*60)
    
    try:
        weather = get_weather_forecast_data()
        print(f"✓ Successfully fetched {len(weather)} days of weather forecast")
        
        if weather:
            print("\nSample weather data:")
            for day in weather[:3]:
                print(f"  - {day['date']}: {day['conditions']}, "
                      f"{day['temp_max']}/{day['temp_min']}°C, "
                      f"{day['precipitation']}mm rain")
        
        formatted = format_weather_for_analysis(weather)
        print(f"\n✓ Successfully formatted weather for analysis")
        print(f"  Preview: {formatted[:200]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error testing weather service: {e}")
        return False


def test_sales_data():
    """Test sales data formatting"""
    print("\n" + "="*60)
    print("TESTING SALES DATA SERVICE")
    print("="*60)
    
    try:
        # Using fallback data for testing
        sales = get_fallback_sales_data()
        print(f"✓ Successfully got sales data ({sales['data_points']} days)")
        print(f"  - Average daily sales: ${sales['avg_daily_sales']:,.2f}")
        print(f"  - Trend: {sales['trend']} ({sales['trend_percentage']:.1f}%)")
        
        formatted = format_sales_for_analysis(sales)
        print(f"\n✓ Successfully formatted sales for analysis")
        print(f"  Preview: {formatted[:200]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error testing sales data: {e}")
        return False


def test_predictive_insights():
    """Test AI insights generation"""
    print("\n" + "="*60)
    print("TESTING PREDICTIVE INSIGHTS GENERATION")
    print("="*60)
    
    try:
        print("Gathering data from all sources...")
        
        # Get all data
        holidays = get_next_30_days_holidays()
        print(f"  ✓ Holidays: {len(holidays)}")
        
        weather = get_weather_forecast_data()
        print(f"  ✓ Weather: {len(weather)} days")
        
        sales = get_fallback_sales_data()
        print(f"  ✓ Sales: {sales['data_points']} days")
        
        print("\nGenerating AI insights with Gemini...")
        insights = generate_predictive_insights(sales, weather, holidays)
        
        print("\n✓ Successfully generated predictive insights!")
        print(f"  - Generated at: {insights.get('generated_at', 'N/A')}")
        print(f"  - Weather insights: {len(insights.get('weather_insights', []))}")
        print(f"  - Holiday insights: {len(insights.get('holiday_insights', []))}")
        print(f"  - Abnormalities: {len(insights.get('abnormalities', []))}")
        print(f"  - Recommendations: {len(insights.get('actionable_recommendations', []))}")
        
        if 'summary' in insights:
            summary = insights['summary']
            print(f"\nSummary:")
            print(f"  - Overall outlook: {summary.get('overall_outlook', 'N/A')}")
            print(f"  - Predicted impact: {summary.get('total_predicted_impact', 'N/A')}")
            print(f"  - Key dates to watch: {len(summary.get('key_dates_to_watch', []))}")
        
        # Show sample insights
        if insights.get('weather_insights'):
            print("\nSample Weather Insight:")
            insight = insights['weather_insights'][0]
            print(f"  Date: {insight.get('date', 'N/A')}")
            print(f"  Prediction: {insight.get('prediction', 'N/A')}")
            print(f"  Impact: {insight.get('impact', 'N/A')}")
        
        if insights.get('actionable_recommendations'):
            print("\nSample Recommendation:")
            rec = insights['actionable_recommendations'][0]
            print(f"  Category: {rec.get('category', 'N/A')}")
            print(f"  Priority: {rec.get('priority', 'N/A')}")
            print(f"  Action: {rec.get('recommendation', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"✗ Error testing predictive insights: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PREDICTIVE ANALYTICS SERVICE - TEST SUITE")
    print("="*60 + "\n")
    
    results = []
    
    # Run all tests
    results.append(("Holiday Service", test_holiday_service()))
    results.append(("Weather Service", test_weather_service()))
    results.append(("Sales Data", test_sales_data()))
    results.append(("Predictive Insights", test_predictive_insights()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The predictive analytics service is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
