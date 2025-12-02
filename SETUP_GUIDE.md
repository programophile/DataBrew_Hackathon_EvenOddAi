# DataBrew Analytics - Setup Guide

This guide will help you connect and run both the backend and frontend of the DataBrew Analytics application.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- MySQL/MariaDB database
- Git

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment (if not already created)
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create/update the `.env` file in the `backend` directory with your configuration:
```
DATABASE_URL=mysql+pymysql://root:@localhost:3306/databrew
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important:**
- Make sure your MySQL database named `databrew` is running and accessible
- Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- The AI insights feature requires a valid Gemini API key

### 6. Test Gemini AI Integration (Optional)
```bash
python test_gemini.py
```

This will verify that:
- The `google-generativeai` package is installed
- Your Gemini API key is configured correctly
- The AI insights generation is working

### 7. Run the Backend Server
```bash
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: http://localhost:8000

You can view the API documentation at: http://localhost:8000/docs

## Frontend Setup

### 1. Navigate to Frontend Directory (in a new terminal)
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment
The frontend is already configured to connect to the backend at `http://localhost:8000`.
You can modify this in the `frontend/.env` file if needed:
```
VITE_API_URL=http://localhost:8000
```

### 4. Run the Frontend Development Server
```bash
npm run dev
```

The frontend will be available at: http://localhost:5173 (or another port if 5173 is busy)

## Testing the Integration

1. **Start the Backend**: Make sure the backend server is running on port 8000
2. **Start the Frontend**: Make sure the frontend dev server is running
3. **Open Browser**: Navigate to http://localhost:5173
4. **Login**: Use the login/signup page (currently mock authentication)
5. **View Dashboard**: You should see the dashboard with live data from the backend API

## API Endpoints

The backend provides the following endpoints:

- `GET /` - API status and available endpoints
- `GET /forecast?days=7` - Sales forecast for next N days
- `GET /ai-insights` - AI-generated insights
- `GET /sales-data?period=month` - Sales trend data (today/week/month)
- `GET /dashboard-metrics` - Key dashboard metrics
- `GET /best-selling` - Best-selling product
- `GET /inventory-predictions` - Inventory demand predictions
- `GET /barista-schedule` - Barista schedule
- `GET /customer-feedback` - Customer feedback

## Troubleshooting

### Backend Issues

**Database Connection Error:**
- Verify MySQL is running
- Check database credentials in backend connection string
- Ensure the `databrew` database exists

**Port Already in Use:**
- Change the port in the uvicorn command: `--port 8001`
- Update the frontend `.env` file accordingly

### Frontend Issues

**Cannot Connect to Backend:**
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Verify the `VITE_API_URL` in frontend `.env` file

**Port Already in Use:**
- Vite will automatically suggest another port
- Or specify a port: `npm run dev -- --port 3000`

## CORS Configuration

The backend is already configured to accept requests from any origin (`allow_origins=["*"]`).
For production, update this in `backend/app/main.py` to only allow your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://yourdomain.com"],  # Update this
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Next Steps

- Import your coffee sales data into the database
- Train and save the SARIMA forecasting model
- Configure real authentication instead of mock login
- Deploy to production server

## Support

For issues or questions, please refer to the project documentation or contact the development team.
