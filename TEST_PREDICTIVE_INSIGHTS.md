# Testing Predictive Insights Feature

## Quick Test Guide

### 1. Verify Backend is Running

```powershell
# Check if backend server is running on port 8080
curl http://localhost:8080/docs
```

Expected: You should see the FastAPI Swagger documentation page.

---

### 2. Test Predictive Insights Endpoint

```powershell
# Test the main predictive insights endpoint
curl http://localhost:8080/predictive-insights
```

**Expected Response Format:**

```json
{
  "status": "success",
  "insights": {
    "summary": "Business outlook for next 7 days...",
    "weather_impact": [...],
    "holiday_opportunities": [...],
    "risks": [...],
    "recommendations": [...]
  },
  "data_sources": {
    "weather_period": "2025-01-15 to 2025-01-21",
    "holidays_checked": 7,
    "sales_period": "Last 7 days"
  },
  "generated_at": "2025-01-15T10:30:00Z"
}
```

---

### 3. Test Individual Data Sources

#### Test Holidays Endpoint

```powershell
curl http://localhost:8080/holidays
```

**Expected**: JSON array with upcoming holidays:

```json
[
  {
    "date": "2025-01-16",
    "name": "Republic Day",
    "local_name": "Republic Day"
  }
]
```

#### Test Weather Forecast Endpoint

```powershell
curl http://localhost:8080/weather-forecast
```

**Expected**: Weather data for next 7 days with temperature, conditions, and precipitation.

---

### 4. Test Frontend Integration

#### Step 1: Start Frontend (if not running)

```powershell
cd f:\DataBrew_Hackathon\frontend
npm run dev
```

#### Step 2: Open Browser

Navigate to: `http://localhost:5173`

#### Step 3: Go to AI Insights Page

- Click on **"AI Insights"** in the sidebar menu
- You should see 3 tabs at the top:
  1. **Predictive Insights** (with cloud/rain icon) ← NEW
  2. **Current Insights** (with sparkles icon)
  3. **Sales Forecast** (with trending up icon)

#### Step 4: View Predictive Insights

- Click on the **"Predictive Insights"** tab
- Wait 2-5 seconds for data to load
- You should see:
  - ✅ **Summary card** at the top with key metrics
  - ✅ **Weather Impact** section (collapsible)
  - ✅ **Holiday Opportunities** section (collapsible)
  - ✅ **Risks & Abnormalities** section (collapsible)
  - ✅ **Actionable Recommendations** section (collapsible)

---

### 5. Verify Data is Being Fetched

#### Open Browser DevTools

1. Press `F12` to open browser console
2. Go to **Network** tab
3. Refresh the page (or click on Predictive Insights tab)
4. Look for a request to: `http://localhost:8080/predictive-insights`
5. Click on it and check:
   - **Status**: Should be `200 OK`
   - **Preview**: Should show JSON data with insights
   - **Response Time**: Should be < 5 seconds

---

### 6. Test Refresh Functionality

1. On the Predictive Insights panel, click the **"Refresh Insights"** button (circular arrow icon in top right)
2. You should see:
   - Loading spinner appears
   - Button text changes to "Refreshing..."
   - After 2-5 seconds, new data appears
   - Success message or updated timestamp

---

### 7. Test Collapsible Sections

Each insight section (Weather, Holidays, Risks, Recommendations) has expand/collapse functionality:

1. Click on the chevron icon (▼/▲) next to section titles
2. Section should smoothly expand or collapse
3. All sections can be expanded simultaneously

---

## Common Issues & Solutions

### ❌ Issue: "Failed to fetch insights"

**Possible Causes:**

1. Backend server not running on port 8080
2. CORS issue between frontend (5173) and backend (8080)
3. Database connection issue

**Solutions:**

```powershell
# Check backend logs
cd f:\DataBrew_Hackathon\backend
# Look at the terminal where you ran: python -m uvicorn app.main:app --reload --port 8080

# Verify .env file has correct keys
cat .env
# Should have: GROG_API_KEY=your_key_here
```

---

### ❌ Issue: "Weather data unavailable"

**Possible Causes:**

1. Weather API key expired or invalid
2. Weather API quota exceeded
3. Network connectivity issue

**Solutions:**

- Check `WEATHER_API_KEY` in `.env` file
- The system has fallback weather data, so it should still work
- Check backend logs for weather API errors

---

### ❌ Issue: "No holidays found"

**Possible Causes:**

1. Holiday API (date.nager.at) is down
2. Network issue
3. No holidays in next 7 days

**Solutions:**

- The system has fallback holiday data
- Try expanding the `days_ahead` parameter to 14 days
- Check backend logs for holiday API errors

---

### ❌ Issue: "Slow response time (>10 seconds)"

**Possible Causes:**

1. Database query is slow (large transactions table)
2. Groq API is slow
3. Too much data being processed

**Solutions:**

```python
# Edit backend/app/predictive_analytics.py
# Reduce data windows:
days_ahead = 3  # Instead of 7
days_back = 3   # Instead of 7

# Reduce token limit:
max_tokens = 1000  # Instead of 1500
```

---

### ❌ Issue: "Database errors"

**Possible Causes:**

1. No recent transaction data (last 7 days)
2. Database connection issue
3. Transactions table schema mismatch

**Solutions:**

```powershell
# Check database connection
cd f:\DataBrew_Hackathon\backend
python check_data.py

# Verify transactions table exists and has data
# Connect to MySQL and run:
# SELECT COUNT(*) FROM transactions WHERE transaction_date >= DATE_SUB(NOW(), INTERVAL 7 DAY);
```

---

## Success Criteria Checklist

- [ ] Backend server running on port 8080
- [ ] `/predictive-insights` endpoint returns valid JSON
- [ ] `/holidays` endpoint returns upcoming holidays
- [ ] `/weather-forecast` endpoint returns 7-day weather data
- [ ] Frontend loads without errors at `localhost:5173`
- [ ] AI Insights page shows 3 tabs
- [ ] Predictive Insights tab loads data successfully
- [ ] All 4 sections (Weather, Holidays, Risks, Recommendations) display data
- [ ] Refresh button works correctly
- [ ] Collapsible sections expand/collapse smoothly
- [ ] No console errors in browser DevTools
- [ ] Response time < 5 seconds

---

## Sample Test Commands (PowerShell)

```powershell
# Full test sequence
Write-Host "Testing Predictive Insights Backend..." -ForegroundColor Cyan

# Test 1: Health check
Write-Host "`n1. Testing backend health..." -ForegroundColor Yellow
curl http://localhost:8080/docs

# Test 2: Predictive insights
Write-Host "`n2. Testing predictive insights endpoint..." -ForegroundColor Yellow
$response = curl http://localhost:8080/predictive-insights | ConvertFrom-Json
$response | ConvertTo-Json -Depth 10

# Test 3: Holidays
Write-Host "`n3. Testing holidays endpoint..." -ForegroundColor Yellow
curl http://localhost:8080/holidays

# Test 4: Weather
Write-Host "`n4. Testing weather forecast endpoint..." -ForegroundColor Yellow
curl http://localhost:8080/weather-forecast

Write-Host "`nAll tests completed!" -ForegroundColor Green
```

---

## Performance Benchmarks

### Expected Response Times:

- `/holidays`: < 500ms (cached) or < 2s (API call)
- `/weather-forecast`: < 1s (API call)
- `/predictive-insights`: 2-5 seconds (AI processing)

### Expected Data Sizes:

- Holidays: ~1-5 KB
- Weather: ~5-10 KB
- Predictive Insights: ~10-30 KB

---

## Next Steps After Successful Testing

1. **Monitor Performance**: Track response times over several days
2. **Collect Feedback**: Ask users if insights are accurate and actionable
3. **Iterate on Prompts**: Improve AI prompts based on feedback
4. **Add Caching**: Implement Redis caching for faster responses
5. **Track Accuracy**: Compare predictions with actual outcomes
6. **Expand Features**: Add more data sources (social media trends, competitor analysis)

---

**Last Updated**: January 15, 2025
**Feature Status**: ✅ Fully Integrated and Ready for Testing
