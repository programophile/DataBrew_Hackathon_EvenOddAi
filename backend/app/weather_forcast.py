import requests
from datetime import datetime, timedelta

# ---- CONFIG ----
API_KEY = "9CP63WBQHDQ2A52ESSE85KWY4"
latitude = 23.7918
longitude = 90.3943

# Generate start and end date (today → next 30 days)
start_date = datetime.today().date()
end_date = start_date + timedelta(days=30)

# Format as YYYY-MM-DD for Visual Crossing
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

# ---- API URL ----
url = (
    f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    f"{latitude},{longitude}/{start_str}/{end_str}"
    f"?unitGroup=metric&key={API_KEY}&contentType=json&include=days,hours,alerts"
)

print("Requesting:", url)

# ---- FETCH DATA ----
response = requests.get(url)

if response.status_code != 200:
    print("Error:", response.text)
    exit()

data = response.json()

# ---- EXTRACT 30-DAY FORECAST ----
forecast_days = data.get("days", [])  # full list of days

print("\n=== 30-Day Weather Forecast ===\n")

for day in forecast_days:
    print(f"Date: {day['datetime']}")
    print(f"  Conditions: {day.get('conditions')}")
    print(f"  Temp (max/min): {day.get('tempmax')}°C / {day.get('tempmin')}°C")
    print(f"  Humidity: {day.get('humidity')}%")
    print(f"  Wind: {day.get('windspeed')} km/h")
    print(f"  Precipitation: {day.get('precip')} mm")
    print("----------------------------------")

# ---- ALERTS ----
print("\n=== WEATHER ALERTS ===")
alerts = data.get("alerts", [])

if alerts:
    for alert in alerts:
        print("Alert:", alert.get("event"))
        print("Headline:", alert.get("headline"))
        print("Description:", alert.get("description"))
        print("----------------------------------")
else:
    print("No alerts found for this period.")
