# DataBrew Analytics - Quick Start Guide

## 🚀 Running the Application (2023-06-24 Date Context)

### Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] MySQL running with `databrew` database
- [ ] Gemini API key obtained from [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## Step 1: Setup Backend (5 minutes)

### Option A: Using Batch File (Windows - Recommended)
```bash
# 1. Install dependencies first
cd backend
pip install -r requirements.txt

# 2. Configure environment
# Edit backend/.env and add:
#   GEMINI_API_KEY=your_actual_key_here

# 3. Run backend
cd ..
start_backend.bat
```

### Option B: Manual Setup
```bash
cd backend

# Activate virtual environment
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start server
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Verify Backend**: Open http://localhost:8000
You should see:
```json
{
  "message": "Coffee Sales Analytics API",
  "status": "running",
  "database": "connected"
}
```

---

## Step 2: Setup Frontend (3 minutes)

### Option A: Using Batch File (Windows - Recommended)
```bash
# 1. Install dependencies (first time only)
cd frontend
npm install

# 2. Run frontend
cd ..
start_frontend.bat
```

### Option B: Manual Setup
```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

**Verify Frontend**: Open http://localhost:5173
You should see the login page.

---

## Step 3: Test the Integration (2 minutes)

### 1. Test Backend API
Open http://localhost:8000/docs

Try these endpoints:
- ✅ `GET /` - Should show "running"
- ✅ `GET /ai-insights` - Should return Gemini AI insights
- ✅ `GET /dashboard-metrics` - Should return metrics for 2023-06-24

### 2. Test Gemini AI
```bash
cd backend
python test_gemini.py
```

Expected output:
```
[1/4] Testing google-generativeai import...
✓ Successfully imported google.generativeai

[2/4] Testing API key configuration...
✓ GEMINI_API_KEY found: AIzaSyCKY...

[3/4] Testing Gemini API connection...
✓ Gemini API connection successful!

[4/4] Testing gemini_service module...
✓ Generated 3 insights:
  1. [trending_up] Cappuccino sales up 15% - consider menu expansion
  2. [users] Need 2 extra baristas during 6-8 PM tomorrow
  3. [clock] Peak customer traffic at 3:00 PM
```

### 3. Test Frontend
1. Open http://localhost:5173
2. Click "Sign Up" or "Login" (mock authentication)
3. You should see the dashboard with:
   - ✅ Metric cards with data from 2023-06-24
   - ✅ AI Insights panel with Gemini-generated recommendations
   - ✅ Sales chart with historical data
   - ✅ Inventory predictions
   - ✅ Barista schedule
   - ✅ Best-selling product

---

## Common Issues & Quick Fixes

### ❌ Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process or use different port
python -m uvicorn main:app --reload --port 8001
```

### ❌ Gemini API not working
```bash
# Verify API key
cd backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"

# Test connection
python test_gemini.py
```

### ❌ Database connection error
```sql
-- Verify database exists
SHOW DATABASES LIKE 'databrew';

-- Create if missing
CREATE DATABASE databrew;

-- Verify tables exist
USE databrew;
SHOW TABLES;
```

### ❌ Frontend can't connect to backend
```bash
# 1. Verify backend is running
curl http://localhost:8000

# 2. Check frontend .env file
cat frontend/.env
# Should contain: VITE_API_URL=http://localhost:8000

# 3. Restart frontend
npm run dev
```

### ❌ No data showing in dashboard
Check your database has data for June 2023 or earlier:
```sql
SELECT
    DATE(transaction_date) as date,
    COUNT(*) as transactions
FROM transactions
WHERE transaction_date <= '2023-06-24'
GROUP BY DATE(transaction_date)
ORDER BY date DESC
LIMIT 10;
```

---

## Verification Checklist

Before reporting issues, verify:
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Database `databrew` exists and is accessible
- [ ] `GEMINI_API_KEY` is set in `backend/.env`
- [ ] Database has transactions before/on 2023-06-24
- [ ] No firewall blocking ports 8000 or 5173
- [ ] Both terminals/command prompts are still running

---

## Quick Commands Reference

### Backend
```bash
# Start backend
cd backend && venv\Scripts\activate && cd app && python -m uvicorn main:app --reload

# Test Gemini
cd backend && python test_gemini.py

# Check logs
# Backend logs appear in the terminal where you ran uvicorn
```

### Frontend
```bash
# Start frontend
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Install new package
cd frontend && npm install <package-name>
```

### Database
```bash
# Connect to MySQL
mysql -u root -p

# Use databrew database
USE databrew;

# Check data for 2023-06-24
SELECT * FROM transactions WHERE DATE(transaction_date) = '2023-06-24' LIMIT 5;
```

---

## Expected Performance

With **2023-06-24** as the current date:

### Dashboard Metrics
- **Total Sales**: Sum of all transactions on 2023-06-24
- **Sales Trend**: % change from 2023-06-23
- **Total Customers**: Unique customers on 2023-06-24
- **Sparkline**: Last 7 days (2023-06-18 to 2023-06-24)

### AI Insights (Gemini)
Based on:
- Last 14 days of data (2023-06-10 to 2023-06-24)
- Top 3 products in that period
- Peak hours analysis
- Week-over-week trends

### Sales Chart
- **Today**: 2023-06-24 only
- **Week**: 2023-06-18 to 2023-06-24 (7 days)
- **Month**: 2023-05-25 to 2023-06-24 (30 days)

---

## Success! What's Next?

Once everything is running:

1. **Explore the Dashboard**: Click through different pages
2. **Test Time Periods**: Try "Today", "Week", "Month" filters
3. **Check AI Insights**: See Gemini's recommendations
4. **Customize**: Edit Gemini prompts in `backend/app/gemini_service.py`

---

## Support

**Documentation**:
- Full setup: `SETUP_GUIDE.md`
- Integration details: `INTEGRATION_SUMMARY.md`
- API docs: http://localhost:8000/docs

**Need Help?**
1. Check backend terminal for error messages
2. Check browser console (F12) for frontend errors
3. Run `python test_gemini.py` to test AI integration
4. Verify database has data: `SELECT COUNT(*) FROM transactions;`

---

**🎉 You're all set! Enjoy your AI-powered coffee shop analytics dashboard!**
