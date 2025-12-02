# Predictive Analytics - Quick Start Guide

## What It Does

Analyzes **holidays + weather + sales history** to predict:

- 📈 Sales opportunities (Valentine's Day, hot weather)
- ⚠️ Risk days (heavy rain, low traffic)
- 💡 Smart recommendations (inventory, staffing, marketing)

## Quick Test

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies (if not already done)
pip install requests

# 3. Run test script
python test_predictive_analytics.py
```

## Use the API

### Start Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Get Insights

```bash
# Full predictive insights (recommended)
curl http://localhost:8000/predictive-insights

# Just holidays
curl http://localhost:8000/holidays

# Just weather
curl http://localhost:8000/weather-forecast
```

## Example Response

```json
{
  "insights": {
    "weather_insights": [
      {
        "date": "2024-12-15",
        "prediction": "Heavy rain expected, 30% drop in foot traffic likely",
        "recommendation": "Boost delivery promos, reduce staff by 2",
        "impact": "negative"
      }
    ],
    "holiday_insights": [
      {
        "holiday_name": "Christmas",
        "expected_sales_increase": "45%",
        "recommendation": "Stock festive drinks, hire 3 temp staff",
        "product_suggestions": ["Peppermint Mocha", "Gingerbread Latte"]
      }
    ],
    "summary": {
      "overall_outlook": "positive",
      "total_predicted_impact": "+12%",
      "top_3_priorities": [
        "Prepare for Christmas rush",
        "Weather-proof operations for rainy week",
        "Launch holiday marketing campaign"
      ]
    }
  }
}
```

## Business Use Cases

| Scenario               | Prediction       | Action                              |
| ---------------------- | ---------------- | ----------------------------------- |
| Valentine's Day        | +45% sales       | Stock romantic drinks, extra staff  |
| Heavy Rain Day         | -30% sales       | Reduce staff, boost delivery        |
| Hot Summer Day (35°C+) | +25% iced drinks | Triple ice stock, promote cold brew |
| Holiday Weekend        | +50% sales       | Full staffing, extended hours       |
| Rainy Holiday          | Mixed impact     | Balance staff, focus on delivery    |

## Key Files

```
backend/
├── app/
│   ├── holiday.py                    # Fetches holidays
│   ├── weather_forcast.py            # Gets weather data
│   ├── predictive_analytics.py       # Main AI service
│   └── main.py                       # API endpoints
└── test_predictive_analytics.py      # Test everything
```

## Environment Setup

Create `backend/.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

Get key: https://makersuite.google.com/app/apikey

## Troubleshooting

**No Gemini API key?**

- Service still works with fallback insights
- Get free key from Google AI Studio

**Holiday API not working?**

- Automatically uses fallback common holidays

**Weather API error?**

- Check API key in `weather_forcast.py`
- Falls back to default patterns

**Database not connected?**

- Uses mock sales data automatically
- Fix connection in `main.py`

## Integration with Frontend

```javascript
// Fetch predictive insights
const response = await fetch("http://localhost:8000/predictive-insights");
const data = await response.json();

// Display insights
data.insights.weather_insights.forEach((insight) => {
  console.log(`${insight.date}: ${insight.prediction}`);
});

// Show recommendations
data.insights.actionable_recommendations.forEach((rec) => {
  console.log(`[${rec.priority}] ${rec.recommendation}`);
});
```

## Performance

- **Response Time**: 5-10 seconds (AI generation)
- **Data Sources**: 3 (holidays, weather, sales)
- **AI Model**: Gemini 2.0 Flash
- **Insights Generated**: 10-15 per request

## Next Steps

1. ✅ Test the service: `python test_predictive_analytics.py`
2. ✅ Start the server: `uvicorn app.main:app --reload`
3. ✅ Test endpoint: Visit `http://localhost:8000/predictive-insights`
4. 🔲 Integrate with frontend dashboard
5. 🔲 Set up automated daily reports
6. 🔲 Add email notifications for high-priority alerts

## Support

- Check logs in terminal
- Review `PREDICTIVE_ANALYTICS_DOCS.md` for detailed info
- Run tests to verify everything works
