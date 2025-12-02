# AI Insights Generate Button Implementation

## Overview
Successfully implemented the "Generate New Insights" button functionality that uses SQL queries and the Gemini API to generate real-time AI-powered business insights for the DataBrew coffee shop analytics dashboard.

## What Was Implemented

### 1. Backend API Endpoint (`backend/app/main.py`)

#### New Helper Function: `fetch_sales_data_for_insights()`
- Executes multiple SQL queries to gather comprehensive data:
  - **Sales trends**: Last 14 days of daily sales, order count, and items sold
  - **Top products**: Last 7 days of best-selling products by revenue
  - **Hourly patterns**: Last 3 days of peak customer traffic hours
  - **Inventory levels**: Low-stock items that need reordering
  - **Week-over-week changes**: Sales trend calculations

#### New POST Endpoint: `/generate-insights`
- **Method**: POST
- **Endpoint**: `http://localhost:8000/generate-insights`
- **Response Format**:
```json
{
  "insights": [
    {
      "type": "trending_up",
      "text": "Iced Latte sales up 12% WoW - stock up on milk and ice",
      "color": "#22c55e"
    }
  ],
  "generated_at": "2023-06-24T10:30:00",
  "data_summary": {
    "avg_daily_sales": 12450.50,
    "trend": "increasing",
    "top_product": "Iced Latte"
  }
}
```

### 2. Enhanced Gemini AI Service (`backend/app/gemini_service.py`)

#### Improved Prompt Engineering
- Added comprehensive sales data context including:
  - Recent sales trends and week-over-week changes
  - Top selling products with revenue figures
  - Peak hour identification
  - Low stock inventory alerts
  - Customer count trends
  - Average order values

#### Insight Types
- **trending_up**: Sales trends and revenue opportunities
- **users**: Staffing optimization recommendations
- **clock**: Time-based insights and peak hour predictions
- **alert**: Urgent inventory and operational alerts

#### Color Coding
- `#22c55e` (green): Positive trends and opportunities
- `#f59e0b` (orange): Warnings and medium priority items
- `#ef4444` (red): Urgent alerts
- `#8b5e3c` (brown): Neutral informational insights

### 3. Frontend API Service (`frontend/src/services/api.ts`)

#### New Function: `generateInsights()`
```typescript
generateInsights: async () => {
  const response = await fetch(`${API_BASE_URL}/generate-insights`, {
    method: "POST",
    headers: { "Content-Type": "application/json" }
  });
  return await response.json();
}
```

### 4. AI Insights Page (`frontend/src/components/pages/AIInsightsPage.tsx`)

#### New Features
- **State Management**:
  - `generating`: Tracks button loading state
  - `liveInsights`: Stores dynamically generated insights

- **Handler Function**: `handleGenerateInsights()`
  - Calls the API to generate fresh insights
  - Maps API response to UI format
  - Updates the insights grid in real-time
  - Shows loading state during generation

- **Button Functionality**:
  - Disabled during generation
  - Shows "Generating..." text while loading
  - Updates all insight cards when complete

### 5. AI Insights Panel (`frontend/src/components/dashboard/AIInsightsPanel.tsx`)

#### New Features
- **Handler Function**: `handleGenerateReport()`
  - Generates insights for the dashboard panel
  - Updates insights in real-time
  - Shows loading state

- **Button Functionality**:
  - "Generate AI Report" button with loading state
  - Disabled during generation

## SQL Queries Used

### 1. Sales Trends Query
```sql
SELECT
    DATE(transaction_date) as date,
    SUM(transaction_qty * unit_price) as daily_sales,
    COUNT(DISTINCT transaction_id) as order_count,
    SUM(transaction_qty) as items_sold
FROM transactions
WHERE transaction_date >= DATE_SUB('2023-06-24', INTERVAL 14 DAY)
GROUP BY DATE(transaction_date)
ORDER BY date DESC
```

### 2. Top Products Query
```sql
SELECT
    product_detail,
    product_type,
    SUM(transaction_qty) as total_qty,
    SUM(transaction_qty * unit_price) as total_revenue,
    COUNT(DISTINCT transaction_id) as order_count
FROM transactions
WHERE transaction_date >= DATE_SUB('2023-06-24', INTERVAL 7 DAY)
GROUP BY product_detail, product_type
ORDER BY total_revenue DESC
LIMIT 5
```

### 3. Hourly Patterns Query
```sql
SELECT
    HOUR(transaction_time) as hour,
    COUNT(DISTINCT transaction_id) as customer_count,
    SUM(transaction_qty * unit_price) as hourly_sales
FROM transactions
WHERE DATE(transaction_date) >= DATE_SUB('2023-06-24', INTERVAL 3 DAY)
GROUP BY HOUR(transaction_time)
ORDER BY hourly_sales DESC
LIMIT 3
```

### 4. Low Stock Inventory Query
```sql
SELECT
    item_name,
    stock,
    reorder_level
FROM inventory
WHERE stock < reorder_level * 1.5
ORDER BY (stock / NULLIF(reorder_level, 0)) ASC
LIMIT 3
```

## How to Test

### 1. Start the Backend Server
```bash
# On Windows
start_backend.bat

# On Linux/Mac
./start_backend.sh
```

The backend will start on `http://localhost:8000`

### 2. Start the Frontend
```bash
# On Windows
start_frontend.bat

# On Linux/Mac
./start_frontend.sh
```

The frontend will start on `http://localhost:5173` (or another port)

### 3. Test the Functionality

#### Option A: AI Insights Page
1. Navigate to the "AI Insights" page from the sidebar
2. Click the "Generate New Insights" button in the header
3. Wait for the insights to generate (button shows "Generating...")
4. The insight cards will update with fresh AI-generated content

#### Option B: Dashboard Panel
1. Go to the main Dashboard page
2. Find the "AI Insights" panel
3. Click the "Generate AI Report" button
4. The panel will refresh with new insights

#### Option C: Direct API Test
```bash
# Test the endpoint directly
curl -X POST http://localhost:8000/generate-insights
```

## Expected Behavior

### Success Case
1. Button shows "Generating..." and becomes disabled
2. Backend fetches data from database using SQL queries
3. Gemini API analyzes the data and generates 3-4 insights
4. Frontend receives and displays the new insights
5. Button re-enables and shows original text

### Error Case
- If generation fails, an alert message appears
- Original insights remain displayed
- Button re-enables for retry

## Example Generated Insights

Based on actual data, the system might generate:

1. **Sales Pattern** (Green)
   - "Iced Latte sales increased 15.3% - stock up on milk and ice for peak hours"

2. **Staffing Alert** (Orange)
   - "Need 2 extra baristas during 5-8 PM based on predicted customer surge"

3. **Peak Hour Prediction** (Brown)
   - "Expected customer peak at 3:00 PM - prepare popular items in advance"

4. **Inventory Alert** (Red)
   - "Cappuccino beans running low - current stock lasts 3 days at consumption rate"

## Architecture Flow

```
User clicks button
    ↓
Frontend calls apiService.generateInsights()
    ↓
POST /generate-insights endpoint
    ↓
fetch_sales_data_for_insights() runs 4 SQL queries
    ↓
Data sent to Gemini API with detailed prompt
    ↓
Gemini returns 3-4 actionable insights
    ↓
Backend formats and returns response
    ↓
Frontend updates UI with new insights
```

## Files Modified

1. `backend/app/main.py` - Added helper function and POST endpoint
2. `backend/app/gemini_service.py` - Enhanced prompt with more data context
3. `frontend/src/services/api.ts` - Added generateInsights function
4. `frontend/src/components/pages/AIInsightsPage.tsx` - Added button handler
5. `frontend/src/components/dashboard/AIInsightsPanel.tsx` - Added button handler

## Environment Variables Required

Ensure `backend/.env` contains:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Database Requirements

The implementation expects these MySQL tables:
- `transactions` - Sales transaction data
- `inventory` - Product inventory levels
- `staff` - Employee information (optional)

## Notes

- The system uses the date '2023-06-24' as the current date reference
- All SQL queries are optimized for performance with proper indexes
- Gemini API responses are validated and fallback insights are provided on error
- The UI shows loading states to provide good user feedback
- Insights are generated fresh each time based on latest database data

## Troubleshooting

### Backend not starting
- Check if Python virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure MySQL database is running and accessible

### Gemini API errors
- Verify API key is correct in `.env` file
- Check API quota limits
- Review console logs for specific error messages

### Frontend not connecting
- Verify backend is running on port 8000
- Check CORS settings in `main.py`
- Ensure `VITE_API_URL` environment variable is set correctly

## Success Criteria

✅ Backend endpoint `/generate-insights` responds successfully
✅ SQL queries execute and return data
✅ Gemini API generates 3-4 relevant insights
✅ Frontend button triggers generation on click
✅ UI updates with new insights in real-time
✅ Loading states work correctly
✅ Error handling prevents app crashes
