# DataBrew Analytics Dashboard

> AI-Powered Coffee Shop Analytics with Gemini AI Integration

A full-stack analytics dashboard for coffee shop management featuring real-time sales tracking, AI-generated insights using Google's Gemini API, inventory predictions, and staff scheduling optimization.

## 🎯 Features

### ✨ AI-Powered Insights
- **Gemini 1.5 Flash Integration**: Intelligent business recommendations
- **Context-Aware Analysis**: Analyzes 14 days of sales patterns
- **Actionable Recommendations**: Staffing, inventory, and sales strategies

### 📊 Real-Time Analytics
- **Sales Dashboard**: Key metrics with day-over-day comparisons
- **Interactive Charts**: Today, Week, Month views with dynamic filtering
- **Sales Forecasting**: SARIMA model predictions
- **Best-Selling Products**: Live tracking with trend analysis

### 📦 Inventory Management
- **AI Demand Prediction**: Smart reorder alerts
- **Stock Level Monitoring**: Critical, warning, and safe indicators
- **Automated Recommendations**: Based on historical patterns

### 👥 Staff Optimization
- **Barista Scheduling**: Performance tracking
- **Peak Hour Analysis**: AI-suggested staffing levels
- **Shift Management**: Visual schedule display

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL Database
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation & Setup

**Option 1: Quick Start (Windows)**
```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Configure environment
# Edit backend/.env with your GEMINI_API_KEY

# 3. Install frontend dependencies
cd ../frontend
npm install

# 4. Start both servers
cd ..
start_backend.bat    # Terminal 1
start_frontend.bat   # Terminal 2
```

**Option 2: See Detailed Instructions**
- 📖 [Complete Setup Guide](SETUP_GUIDE.md)
- 🚀 [Quick Start Guide](QUICK_START.md)
- 🔗 [Integration Details](INTEGRATION_SUMMARY.md)

### Access Points
- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📅 Date Configuration

The application is configured to use **June 24, 2023** as the current date for historical data analysis. This ensures consistent results with your dataset.

All queries automatically use this fixed date:
- Dashboard metrics: Data for 2023-06-24
- Trends: Comparison with 2023-06-23
- Weekly data: 2023-06-18 to 2023-06-24
- Monthly data: 2023-05-25 to 2023-06-24

## 🏗️ Architecture

### Backend (FastAPI + Python)
```
backend/
├── app/
│   ├── main.py              # API endpoints
│   ├── gemini_service.py    # AI insights generation
│   └── utlis/               # Utility functions
├── models/                   # ML models
├── database/                 # Database schemas
├── test_gemini.py           # Gemini integration tests
└── requirements.txt         # Python dependencies
```

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/
│   │   ├── dashboard/       # Dashboard widgets
│   │   ├── pages/           # Page components
│   │   └── ui/              # UI components (shadcn)
│   ├── services/
│   │   └── api.ts           # API service layer
│   └── App.tsx              # Main application
└── package.json
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status and info |
| `/ai-insights` | GET | Gemini AI-generated insights ✨ |
| `/dashboard-metrics` | GET | Key dashboard metrics |
| `/sales-data?period={period}` | GET | Sales trend data |
| `/forecast?days={n}` | GET | Sales forecast (n days) |
| `/best-selling` | GET | Best-selling product |
| `/inventory-predictions` | GET | AI inventory predictions |
| `/barista-schedule` | GET | Staff schedule |
| `/customer-feedback` | GET | Customer reviews |
| `/docs` | GET | Interactive API docs |

## 🧠 Gemini AI Integration

### How It Works
1. Backend queries sales data from MySQL database
2. `prepare_sales_summary()` creates context with:
   - Sales trends and patterns
   - Top products
   - Peak hours
   - Week-over-week changes
3. `generate_ai_insights()` sends context to Gemini API
4. Gemini returns 3-4 actionable insights
5. Frontend displays insights in AI Insights Panel

### Example Insights
```json
{
  "insights": [
    {
      "type": "trending_up",
      "text": "Cappuccino sales up 18% - expand variety",
      "color": "#22c55e"
    },
    {
      "type": "users",
      "text": "Add 2 baristas for 6-8 PM rush tomorrow",
      "color": "#f59e0b"
    },
    {
      "type": "clock",
      "text": "Peak traffic predicted at 3:00 PM",
      "color": "#8b5e3c"
    }
  ]
}
```

### Testing Gemini Integration
```bash
cd backend
python test_gemini.py
```

## 🎨 Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: MySQL + SQLAlchemy
- **AI**: Google Gemini 1.5 Flash
- **ML**: SARIMA for forecasting
- **Data**: Pandas, NumPy

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Radix UI + Tailwind CSS
- **Charts**: Recharts
- **State**: React Hooks

## 📊 Dashboard Components

### 1. Metric Cards
- Total Sales (Today)
- Total Customers
- Net Profit Margin
- Active Baristas Needed

### 2. AI Insights Panel ✨
- Real-time Gemini AI recommendations
- Trend analysis
- Staffing suggestions
- Peak hour predictions

### 3. Sales Charts
- Interactive line charts
- Period filters (Today/Week/Month)
- Historical comparison

### 4. Inventory Table
- Stock levels
- AI demand predictions
- Reorder alerts (Critical/Warning/Safe)

### 5. Barista Schedule
- Staff shifts
- Performance metrics
- Visual indicators

### 6. Best Selling Widget
- Top product of the day
- Units sold & revenue
- Day-over-day comparison

## 🔧 Configuration

### Backend Environment (`.env`)
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=mysql+pymysql://root:@localhost:3306/databrew
```

### Frontend Environment (`.env`)
```env
VITE_API_URL=http://localhost:8000
```

## 🧪 Testing

### Test Gemini AI
```bash
cd backend
python test_gemini.py
```

### Test API Endpoints
Visit: http://localhost:8000/docs

### Test Frontend
```bash
cd frontend
npm run dev
```
Open: http://localhost:5173

## 📚 Documentation

- **[Setup Guide](SETUP_GUIDE.md)**: Detailed installation instructions
- **[Quick Start](QUICK_START.md)**: Get running in 10 minutes
- **[Integration Summary](INTEGRATION_SUMMARY.md)**: Technical architecture details

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check database connection
mysql -u root -p -e "SHOW DATABASES LIKE 'databrew';"

# Verify Gemini API key
cd backend
python test_gemini.py

# Check logs
# Backend logs appear in the uvicorn terminal
```

### Frontend Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check API connection
curl http://localhost:8000
```

## 🚧 Known Limitations

- Mock authentication (no real user management yet)
- Fixed date context (2023-06-24)
- Requires historical data before June 2023
- SARIMA model needs training data

## 🔮 Future Enhancements

- [ ] Real user authentication with JWT
- [ ] Dynamic date selection
- [ ] Export reports to PDF
- [ ] Mobile-responsive design
- [ ] Email notifications for alerts
- [ ] Multi-location support
- [ ] Advanced ML models (Prophet, LSTM)

## 📝 License

This project was created for the DataBrew Hackathon.

## 🙏 Acknowledgments

- **Google Gemini AI**: For intelligent insights generation
- **FastAPI**: For the excellent backend framework
- **Radix UI**: For accessible component primitives
- **Recharts**: For beautiful data visualizations

---

## 📞 Support

For questions or issues:
1. Check the [Setup Guide](SETUP_GUIDE.md)
2. Review API docs at http://localhost:8000/docs
3. Test Gemini integration with `python test_gemini.py`
4. Check backend logs in the uvicorn terminal

---

**Built with ❤️ for DataBrew Hackathon**

**Status**: ✅ Fully Integrated | **Date**: 2023-06-24 | **AI**: Gemini 1.5 Flash
