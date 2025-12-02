"""
Test script for Gemini AI integration
Run this to verify Gemini API is working correctly
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_import():
    """Test if google-generativeai can be imported"""
    try:
        import google.generativeai as genai
        print("✓ Successfully imported google.generativeai")
        return True
    except ImportError as e:
        print(f"✗ Failed to import google.generativeai: {e}")
        print("  Run: pip install google-generativeai")
        return False

def test_api_key():
    """Test if Gemini API key is configured"""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✓ GEMINI_API_KEY found: {api_key[:10]}...")
        return True
    else:
        print("✗ GEMINI_API_KEY not found in environment variables")
        print("  Add GEMINI_API_KEY to backend/.env file")
        return False

def test_gemini_connection():
    """Test if Gemini API connection works"""
    try:
        import google.generativeai as genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return False

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Simple test prompt
        response = model.generate_content("Say 'Hello from Gemini!' in exactly 3 words.")
        print(f"✓ Gemini API connection successful!")
        print(f"  Response: {response.text}")
        return True
    except Exception as e:
        print(f"✗ Gemini API connection failed: {str(e)}")
        return False

def test_gemini_service():
    """Test the gemini_service module"""
    try:
        # Add app directory to path
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

        from gemini_service import generate_ai_insights, prepare_sales_summary

        # Test with sample data
        sample_data = {
            'avg_daily_sales': 8500,
            'trend': 'increasing',
            'wow_change': 8.5,
            'top_products': ['Iced Latte', 'Cappuccino', 'Espresso'],
            'peak_hours': '3:00 PM',
            'customer_trend': 'growing'
        }

        print("✓ Successfully imported gemini_service")
        print(f"  Testing AI insights generation...")

        insights = generate_ai_insights(sample_data)

        print(f"✓ Generated {len(insights)} insights:")
        for i, insight in enumerate(insights, 1):
            print(f"  {i}. [{insight['type']}] {insight['text']}")

        return True
    except Exception as e:
        print(f"✗ Failed to test gemini_service: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Gemini AI Integration")
    print("=" * 60)
    print()

    results = []

    print("[1/4] Testing google-generativeai import...")
    results.append(test_gemini_import())
    print()

    print("[2/4] Testing API key configuration...")
    results.append(test_api_key())
    print()

    print("[3/4] Testing Gemini API connection...")
    results.append(test_gemini_connection())
    print()

    print("[4/4] Testing gemini_service module...")
    results.append(test_gemini_service())
    print()

    print("=" * 60)
    if all(results):
        print("✓ All tests passed! Gemini AI is ready to use.")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
