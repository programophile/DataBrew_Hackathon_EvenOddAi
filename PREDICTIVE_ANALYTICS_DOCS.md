# Predictive Analytics Service Documentation

## Overview

The Predictive Analytics Service integrates **holiday data**, **weather forecasts**, and **historical sales data** to generate AI-powered insights using Google's Gemini AI. This service helps predict sales patterns, identify opportunities, and mitigate risks for the coffee shop business.

## Architecture

### Components

1. **holiday.py** - Fetches upcoming holidays (next 30 days)
2. **weather_forcast.py** - Gets weather forecast (next 30 days)
3. **predictive_analytics.py** - Main service combining all data sources
4. **main.py** - FastAPI endpoints for accessing insights

### Data Flow

```
┌─────────────────┐
│  Holiday API    │──┐
│  (30 days)      │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │    ┌──────────────────┐    ┌─────────────┐
│  Weather API    │──┼───▶│  Predictive      │───▶│  Gemini AI  │
│  (30 days)      │  │    │  Analytics       │    │  Analysis   │
└─────────────────┘  │    │  Service         │    └─────────────┘
                     │    └──────────────────┘           │
┌─────────────────┐  │                                   │
│  Sales DB       │──┘                                   ▼
│  (60 days)      │                            ┌─────────────────┐
└─────────────────┘                            │  AI Insights    │
                                               │  - Weather      │
                                               │  - Holidays     │
                                               │  - Abnormalities│
                                               │  - Actions      │
                                               └─────────────────┘
```

## API Endpoints

### 1. `/predictive-insights` (Main Endpoint)

**GET** request that returns comprehensive predictive insights.

**Response Structure:**

```json
{
  "status": "success",
  "insights": {
    "weather_insights": [
      {
        "date": "2024-12-10",
        "impact": "negative",
        "prediction": "Heavy rain expected, 30% sales decrease likely",
        "recommendation": "Reduce staffing, promote delivery",
        "confidence": "high"
      }
    ],
    "holiday_insights": [
      {
        "holiday_name": "Christmas",
        "date": "2024-12-25",
        "expected_sales_increase": "45%",
        "recommendation": "Stock festive drinks, extra staff",
        "product_suggestions": ["Peppermint Mocha", "Eggnog Latte"]
      }
    ],
    "abnormalities": [
      {
        "date": "2024-12-20",
        "type": "risk",
        "description": "Heavy rain on holiday eve",
        "impact": "20-30% lower foot traffic",
        "mitigation": "Boost online orders, delivery promos"
      }
    ],
    "actionable_recommendations": [
      {
        "category": "inventory",
        "priority": "high",
        "recommendation": "Order 50% more iced coffee supplies",
        "expected_outcome": "Meet 40% demand increase",
        "timeframe": "Next 3 days"
      }
    ],
    "summary": {
      "overall_outlook": "positive",
      "total_predicted_impact": "+12%",
      "key_dates_to_watch": ["2024-12-25", "2024-12-31"],
      "top_3_priorities": [
        "Prepare for Christmas rush",
        "Stock up before rainy week",
        "Launch holiday promotions"
      ]
    }
  },
  "data_summary": {
    "holidays_count": 5,
    "weather_days": 30,
    "sales_days_analyzed": 60
  }
}
```

### 2. `/holidays`

**GET** request to fetch upcoming holidays.

**Parameters:**

- `days` (optional, default=30): Number of days to look ahead

**Response:**

```json
{
  "holidays": [
    {
      "date": "2024-12-25",
      "name": "Christmas Day",
      "localName": "Christmas",
      "type": "Public",
      "global": true
    }
  ],
  "count": 5,
  "period_days": 30
}
```

### 3. `/weather-forecast`

**GET** request to fetch weather forecast.

**Parameters:**

- `days` (optional, default=30): Number of days to forecast

**Response:**

```json
{
  "forecast": [
    {
      "date": "2024-12-10",
      "conditions": "Heavy rain",
      "temp_max": 28,
      "temp_min": 22,
      "humidity": 85,
      "wind_speed": 20,
      "precipitation": 15,
      "precipitation_probability": 90
    }
  ],
  "count": 30,
  "period_days": 30
}
```

## Key Features

### 1. Weather Impact Analysis

- Identifies rainy days that may reduce foot traffic
- Detects hot days that increase iced beverage demand
- Suggests inventory adjustments based on weather

### 2. Holiday Opportunity Detection

- Predicts sales increases for holidays
- Recommends holiday-specific products
- Suggests staffing levels for holiday periods

### 3. Abnormality Detection

- Identifies unusual patterns (e.g., rain on holiday)
- Flags potential risks and opportunities
- Provides mitigation strategies

### 4. Actionable Recommendations

- Inventory management suggestions
- Staffing optimization
- Marketing campaign ideas
- Operational adjustments

## Business Impact Examples

### Scenario 1: Valentine's Day + Good Weather

```
Holiday: Valentine's Day (Feb 14)
Weather: Clear, 25°C, sunny
Historical: +45% sales on Valentine's

AI Prediction:
- Expected sales increase: 50%
- Recommended products: Romantic-themed drinks, heart-shaped pastries
- Staffing: +3 baristas for evening shift
- Inventory: Double stock on milk, chocolate syrup, whipped cream
```

### Scenario 2: Heavy Rain on Weekend

```
Weather: Heavy rain (20mm), 80% humidity
Day: Saturday (normally high traffic)
Historical: -25% sales on rainy weekends

AI Prediction:
- Expected sales decrease: 30%
- Recommendation: Launch delivery promotion, reduce staffing
- Opportunity: Promote hot beverages, comfort drinks
- Action: Boost online marketing for delivery
```

### Scenario 3: Independence Day + Hot Weather

```
Holiday: Independence Day
Weather: Very hot (38°C), sunny
Historical: +30% sales on national holidays

AI Prediction:
- Expected sales increase: 60% (holiday + heat)
- Recommended products: Iced coffee, cold brew, smoothies
- Staffing: Full staff + 2 extra baristas
- Inventory: Triple iced drink supplies, ice stock
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create `.env` file in `backend/` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

### 3. Run Tests

```bash
cd backend
python test_predictive_analytics.py
```

### 4. Start the Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 5. Test the Endpoints

```bash
# Get predictive insights
curl http://localhost:8000/predictive-insights

# Get holidays only
curl http://localhost:8000/holidays

# Get weather forecast only
curl http://localhost:8000/weather-forecast
```

## Configuration

### Holiday API

- Uses free public holiday API: https://date.nager.at/api
- Default country: Bangladesh (BD)
- Change country code in `holiday.py`:
  ```python
  DEFAULT_COUNTRY_CODE = "US"  # For United States
  DEFAULT_COUNTRY_CODE = "IN"  # For India
  ```

### Weather API

- Uses Visual Crossing Weather API
- Current location: Dhaka, Bangladesh (23.7918, 90.3943)
- Change location in `predictive_analytics.py`:
  ```python
  latitude = 40.7128   # New York
  longitude = -74.0060
  ```

### Database Connection

- Uses MySQL/MariaDB
- Connection string in `main.py`:
  ```python
  engine = create_engine("mysql+pymysql://root:@localhost:3306/databrew")
  ```

## Error Handling

All services include fallback mechanisms:

1. **Holiday API fails** → Returns common holidays list
2. **Weather API fails** → Returns default weather patterns
3. **Database unavailable** → Returns mock sales data
4. **Gemini API fails** → Returns template insights

## Performance Considerations

- **Holiday data**: Cached for the day (API rate limit: unlimited)
- **Weather data**: Updated every 6 hours (API rate limit: 1000 calls/day)
- **Sales data**: Real-time database queries
- **AI insights**: Generated on-demand (~5-10 seconds response time)

## Future Enhancements

1. **Caching**: Implement Redis cache for API responses
2. **Webhooks**: Real-time weather alerts
3. **Machine Learning**: Local ML models for faster predictions
4. **Historical Correlation**: Learn from past weather-sales patterns
5. **Multi-location**: Support for multiple shop locations
6. **Custom Events**: Add local events, festivals, sports games

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution**: Create `.env` file with your API key

### Issue: Holiday API returns empty list

**Solution**: Check internet connection or use fallback data

### Issue: Weather API error 401

**Solution**: Verify API key in `weather_forcast.py`

### Issue: Database connection failed

**Solution**: Check MySQL is running and credentials are correct

## Support

For issues or questions:

1. Check the test script: `python test_predictive_analytics.py`
2. Review logs in console output
3. Verify all API keys are set correctly
4. Ensure all dependencies are installed

## License

Part of DataBrew Hackathon Project
