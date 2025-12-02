# DataBrew Analytics - Backend-Frontend Integration Summary

## Overview
This document summarizes the complete integration between the FastAPI backend and React frontend with Gemini AI for intelligent insights.

## Fixed Date Configuration
**Current Date**: `2023-06-24`

All date-dependent queries in the backend have been configured to use this fixed date instead of dynamic dates. This ensures consistent data analysis based on your historical dataset.

## Backend Configuration

### Date Updates Applied
All endpoints now use the fixed date `2023-06-24`:

1. **Dashboard Metrics** (`/dashboard-metrics`)
   - Today's sales: `DATE(transaction_date) = '2023-06-24'`
   - Yesterday's sales: `DATE_SUB('2023-06-24', INTERVAL 1 DAY)`
   - Last 7 days sparkline: `DATE_SUB('2023-06-24', INTERVAL 7 DAY)`

2. **AI Insights** (`/ai-insights`)
   - Recent data (14 days): `DATE_SUB('2023-06-24', INTERVAL 14 DAYS)`

3. **Sales Data** (`/sales-data`)
   - Period-based queries use: `DATE_SUB('2023-06-24', INTERVAL %s DAY)`

4. **Best Selling** (`/best-selling`)
   - Today's best seller: `DATE(transaction_date) = '2023-06-24'`
   - Yesterday's comparison: `DATE_SUB('2023-06-24', INTERVAL 1 DAY)`

### Gemini AI Integration

#### Features
- **Intelligent Insights**: Uses Gemini 1.5 Flash model to analyze sales data
- **Contextual Analysis**: Analyzes trends, peak hours, staffing needs
- **Actionable Recommendations**: Provides specific business recommendations
- **Fallback Support**: Returns default insights if API is unavailable

#### How It Works
1. Backend queries sales data from database
2. `prepare_sales_summary()` creates analysis summary with:
   - Average daily sales
   - Sales trends (increasing/decreasing/steady)
   - Top 3 products
   - Peak hours
   - Week-over-week changes
3. `generate_ai_insights()` sends context to Gemini API
4. Gemini returns 3-4 actionable insights with:
   - Icon type (trending_up, users, clock, alert)
   - Insight text (max 80 characters)
   - Color coding for visual hierarchy

## Frontend Integration

### API Service Layer
Location: `frontend/src/services/api.ts`

All API calls are centralized with:
- Base URL configuration from environment
- TypeScript type safety
- Error handling
- Consistent fetch patterns

### Connected Components

1. **Dashboard Page** (`DashboardPage.tsx`)
   - Fetches metrics from `/dashboard-metrics`
   - Updates metric cards with real data
   - Shows loading states

2. **AI Insights Panel** (`AIInsightsPanel.tsx`)
   - Fetches insights from `/ai-insights`
   - Displays Gemini-generated recommendations
   - Icon mapping for visualization

3. **Sales Chart** (`SalesChart.tsx`)
   - Fetches sales data with period filter
   - Supports: Today, Week, Month views
   - Real-time period switching

4. **Inventory Table** (`InventoryTable.tsx`)
   - Fetches from `/inventory-predictions`
   - Shows stock levels and demand predictions
   - Alert indicators (critical/warning/safe)

5. **Barista Schedule** (`BaristaSchedule.tsx`)
   - Fetches from `/barista-schedule`
   - Shows staff shifts and performance
   - Visual performance indicators

6. **Best Selling** (`BestSelling.tsx`)
   - Fetches from `/best-selling`
   - Shows top product of the day
   - Day-over-day comparison

## API Endpoints

### Available Endpoints

```
GET /                          - API status and endpoints list
GET /forecast?days=7           - Sales forecast (SARIMA model)
GET /ai-insights               - Gemini AI-generated insights ✨
GET /sales-data?period=month   - Sales trend data (today/week/month)
GET /dashboard-metrics         - Dashboard KPIs
GET /best-selling              - Best-selling product
GET /inventory-predictions     - AI inventory demand forecast
GET /barista-schedule          - Staff schedule
GET /customer-feedback         - Customer reviews
GET /docs                      - Interactive API documentation
```

### Response Formats

#### AI Insights Response
```json
{
  "insights": [
    {
      "type": "trending_up",
      "text": "Cappuccino sales increased by 15% this week",
      "color": "#22c55e"
    },
    {
      "type": "users",
      "text": "Add 2 baristas for 6-8 PM rush tomorrow",
      "color": "#f59e0b"
    }
  ]
}
```

#### Dashboard Metrics Response
```json
{
  "total_sales": 12540.50,
  "sales_trend": 8.2,
  "total_customers": 320,
  "profit_margin": 22,
  "active_baristas": 3,
  "sales_sparkline": [8200, 8500, 9100, 8800, 9300, 10200, 12540]
}
```

## Environment Configuration

### Backend (`.env`)
```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=mysql+pymysql://root:@localhost:3306/databrew
```

### Frontend (`.env`)
```
VITE_API_URL=http://localhost:8000
```

## Running the Application

### Quick Start (Windows)
```bash
# Terminal 1 - Backend
start_backend.bat

# Terminal 2 - Frontend
start_frontend.bat
```

### Manual Start
```bash
# Backend
cd backend
venv\Scripts\activate
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Testing

### Test Gemini Integration
```bash
cd backend
python test_gemini.py
```

This validates:
- ✓ Google Generative AI package installed
- ✓ API key configured
- ✓ Gemini API connection working
- ✓ Insights generation functional

### Test Backend Endpoints
Visit: http://localhost:8000/docs

Try these endpoints:
1. `GET /ai-insights` - Test Gemini AI
2. `GET /dashboard-metrics` - Test metrics for 2023-06-24
3. `GET /sales-data?period=week` - Test sales data

## Data Flow

```
Database (MySQL)
    ↓
Backend API (FastAPI)
    ↓
Fixed Date: 2023-06-24
    ↓
Query Historical Data
    ↓
Gemini AI Analysis ✨
    ↓
JSON Response
    ↓
Frontend (React + TypeScript)
    ↓
Dashboard Components
    ↓
User Interface
```

## Key Features

### ✨ AI-Powered
- Gemini 1.5 Flash for intelligent insights
- Context-aware recommendations
- Real-time analysis

### 📊 Real-Time Data
- Live database connections
- Automatic data refresh
- Loading states for UX

### 🎨 Modern UI
- React + TypeScript
- Tailwind CSS styling
- Responsive design
- Smooth transitions

### 🔒 Production-Ready
- CORS configured
- Error handling
- Fallback mechanisms
- Environment-based config

## Troubleshooting

### Issue: Gemini API Not Working
**Solution**:
1. Verify API key in `backend/.env`
2. Run `python test_gemini.py`
3. Check console for error messages

### Issue: No Data Showing
**Solution**:
1. Verify database has data for 2023-06-24 or earlier
2. Check backend console for SQL errors
3. Verify database connection in backend

### Issue: CORS Errors
**Solution**:
1. Verify backend is running on port 8000
2. Check `allow_origins` in `main.py`
3. Clear browser cache

## Next Steps

1. **Import Data**: Ensure your database has transactions from 2023-06-24 or earlier
2. **Customize Insights**: Adjust Gemini prompts in `gemini_service.py`
3. **Add Features**: Extend endpoints for additional analytics
4. **Deploy**: Configure for production environment

## Support

For questions or issues:
1. Check logs in backend console
2. Verify all environment variables
3. Test endpoints at `/docs`
4. Review this documentation

---

**Status**: ✅ Fully Integrated
**Date Context**: 2023-06-24 (Fixed)
**AI Model**: Gemini 1.5 Flash
**Last Updated**: 2024
