"""
Holiday Detection Service
Fetches holidays for the next 30 days using a public holiday API
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict

# Using Calendarific API (free tier available) or Abstract API
# For demonstration, using a free holidays API
HOLIDAYS_API_URL = "https://date.nager.at/api/v3/PublicHolidays"

# Default country code (US for API, but use BD fallback holidays)
DEFAULT_COUNTRY_CODE = "US"  # Changed from BD since BD is not available in the API


def get_next_30_days_holidays(country_code: str = DEFAULT_COUNTRY_CODE) -> List[Dict]:
    """
    Fetch holidays for the next 7 days
    
    Args:
        country_code: ISO 3166-1 alpha-2 country code (US, IN, etc.)
    
    Returns:
        List of holiday dictionaries with date, name, and type
    """
    # Since Bangladesh (BD) is not available in the API, use fallback holidays
    # You can try the API for other countries, but default to Bangladesh holidays
    if country_code == "BD" or country_code == DEFAULT_COUNTRY_CODE:
        return get_fallback_holidays()
    
    try:
        # Get current year and next year
        current_date = datetime.now()
        current_year = current_date.year
        next_year = current_year + 1
        end_date = current_date + timedelta(days=7)
        
        holidays = []
        
        # Fetch holidays for current year
        url_current = f"{HOLIDAYS_API_URL}/{current_year}/{country_code}"
        response_current = requests.get(url_current, timeout=10)
        
        if response_current.status_code == 200:
            holidays.extend(response_current.json())
        else:
            # API failed, use fallback
            return get_fallback_holidays()
        
        # If date range spans into next year, fetch next year's holidays too
        if end_date.year > current_year:
            url_next = f"{HOLIDAYS_API_URL}/{next_year}/{country_code}"
            response_next = requests.get(url_next, timeout=10)
            
            if response_next.status_code == 200:
                holidays.extend(response_next.json())
        
        # Filter holidays within next 7 days
        filtered_holidays = []
        for holiday in holidays:
            holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
            
            if current_date.date() <= holiday_date.date() <= end_date.date():
                filtered_holidays.append({
                    'date': holiday['date'],
                    'name': holiday['name'],
                    'localName': holiday.get('localName', holiday['name']),
                    'type': holiday.get('types', ['Public'])[0] if holiday.get('types') else 'Public',
                    'global': holiday.get('global', True),
                    'counties': holiday.get('counties', None)
                })
        
        # If no holidays found in next 7 days, return empty list (not fallback)
        return filtered_holidays
        
    except requests.RequestException as e:
        print(f"Error fetching holidays: {e}")
        return get_fallback_holidays()
    except Exception as e:
        print(f"Unexpected error in holiday service: {e}")
        return get_fallback_holidays()


def get_fallback_holidays() -> List[Dict]:
    """
    Returns Bangladesh public holidays (BD is not in the API, so using comprehensive fallback)
    """
    current_date = datetime.now()
    current_year = current_date.year
    
    # Bangladesh Public Holidays 2025 (actual dates)
    common_holidays = [
        {'date': f'{current_year}-02-21', 'name': 'Shaheed Dibosh (Martyrs\' Day)', 'type': 'Public'},
        {'date': f'{current_year}-03-17', 'name': 'Sheikh Mujibur Rahman\'s Birthday', 'type': 'Public'},
        {'date': f'{current_year}-03-26', 'name': 'Independence Day', 'type': 'Public'},
        {'date': f'{current_year}-03-31', 'name': 'Eid ul-Fitr', 'type': 'Public'},
        {'date': f'{current_year}-04-01', 'name': 'Eid ul-Fitr Holiday', 'type': 'Public'},
        {'date': f'{current_year}-04-02', 'name': 'Eid ul-Fitr Holiday', 'type': 'Public'},
        {'date': f'{current_year}-04-14', 'name': 'Bengali New Year (Pohela Boishakh)', 'type': 'Public'},
        {'date': f'{current_year}-05-01', 'name': 'May Day', 'type': 'Public'},
        {'date': f'{current_year}-06-07', 'name': 'Eid ul-Adha', 'type': 'Public'},
        {'date': f'{current_year}-06-08', 'name': 'Eid ul-Adha Holiday', 'type': 'Public'},
        {'date': f'{current_year}-06-09', 'name': 'Eid ul-Adha Holiday', 'type': 'Public'},
        {'date': f'{current_year}-07-06', 'name': 'Ashura', 'type': 'Public'},
        {'date': f'{current_year}-08-15', 'name': 'National Mourning Day', 'type': 'Public'},
        {'date': f'{current_year}-09-05', 'name': 'Eid-e-Milad-un-Nabi', 'type': 'Public'},
        {'date': f'{current_year}-12-05', 'name': 'Pohela Aghran (Winter Festival)', 'type': 'Observance'},
        {'date': f'{current_year}-12-16', 'name': 'Victory Day', 'type': 'Public'},
        {'date': f'{current_year}-12-25', 'name': 'Christmas Day', 'type': 'Public'},
        {'date': f'{current_year}-12-31', 'name': 'New Year\'s Eve', 'type': 'Observance'},
        # Next year's holidays for continuity
        {'date': f'{current_year + 1}-01-01', 'name': 'New Year\'s Day', 'type': 'Public'},
        {'date': f'{current_year + 1}-02-21', 'name': 'Shaheed Dibosh (Martyrs\' Day)', 'type': 'Public'},
    ]
    
    # Filter for next 30 days
    end_date = current_date + timedelta(days=7)
    filtered = []
    
    for holiday in common_holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
        if current_date.date() <= holiday_date.date() <= end_date.date():
            filtered.append({
                'date': holiday['date'],
                'name': holiday['name'],
                'localName': holiday['name'],
                'type': holiday['type'],
                'global': True,
                'counties': None
            })
    
    return filtered


def format_holidays_for_analysis(holidays: List[Dict]) -> str:
    """
    Format holidays data into a readable string for AI analysis
    
    Args:
        holidays: List of holiday dictionaries
    
    Returns:
        Formatted string describing upcoming holidays
    """
    if not holidays:
        return "No holidays in next 7 days."
    
    holiday_text = f"Holidays (7 days): {len(holidays)} total\\n"
    
    for holiday in holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
        days_until = (holiday_date.date() - datetime.now().date()).days
        
        holiday_text += f"- {holiday['name']} on {holiday['date']} "
        holiday_text += f"({days_until} days from now, {holiday['type']})\n"
    
    return holiday_text


if __name__ == "__main__":
    # Test the holiday service
    print("Fetching holidays for the next 30 days...")
    holidays = get_next_30_days_holidays()
    
    print(f"\nFound {len(holidays)} holidays:\n")
    for holiday in holidays:
        print(f"📅 {holiday['date']}: {holiday['name']} ({holiday['type']})")
    
    print("\n" + "="*50)
    print("\nFormatted for AI Analysis:")
    print(format_holidays_for_analysis(holidays))
