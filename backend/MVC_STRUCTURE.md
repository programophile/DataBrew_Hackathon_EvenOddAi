# DataBrew Backend - MVC Architecture

## Overview

The backend has been reorganized following the **MVC (Model-View-Controller)** design pattern for better code organization, maintainability, and scalability.

## Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main_mvc.py                 # New MVC-based main application (use this!)
│   ├── main.py                     # Old monolithic main file (deprecated)
│   │
│   ├── config/                     # Configuration Layer
│   │   ├── __init__.py
│   │   ├── database.py            # Database connection & session management
│   │   └── settings.py            # Application settings & environment variables
│   │
│   ├── models/                     # Model Layer (Data structures)
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication models (User, Session)
│   │   └── schemas.py             # Pydantic schemas for validation
│   │
│   ├── services/                   # Service Layer (Business Logic)
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication business logic
│   │   ├── sales_service.py       # Sales data processing
│   │   ├── analytics_service.py   # Analytics & reporting logic
│   │   ├── gemini_service.py      # AI insights with Gemini/Groq
│   │   ├── predictive_service.py  # Predictive analytics
│   │   ├── holiday_service.py     # Holiday data service
│   │   └── weather_service.py     # Weather forecast service
│   │
│   ├── controllers/                # Controller Layer (Request Handlers)
│   │   ├── __init__.py
│   │   ├── auth_controller.py     # Authentication request handlers
│   │   ├── sales_controller.py    # Sales request handlers
│   │   ├── analytics_controller.py # Analytics request handlers
│   │   ├── settings_controller.py # Settings request handlers
│   │   └── inventory_controller.py # Inventory request handlers
│   │
│   ├── routes/                     # Route Layer (API Endpoints)
│   │   ├── __init__.py
│   │   ├── auth_routes.py         # Authentication endpoints
│   │   ├── sales_routes.py        # Sales endpoints
│   │   ├── analytics_routes.py    # Analytics endpoints
│   │   ├── settings_routes.py     # Settings endpoints
│   │   ├── inventory_routes.py    # Inventory endpoints
│   │   └── ai_routes.py           # AI insights endpoints
│   │
│   └── utils/                      # Utility Layer
│       ├── __init__.py
│       └── model_loader.py        # ML model loading utilities
│
├── database/                       # Database files
│   ├── coffee_shop_final.db       # SQLite database
│   └── setup_ingredients.py       # Database setup scripts
│
├── models/                         # ML Models
│   └── sarima_model_forcast.pkl   # Pre-trained SARIMA model
│
├── .env                           # Environment variables
└── requirements.txt               # Python dependencies
```

## Architecture Layers

### 1. **Config Layer** (`app/config/`)
- **Purpose**: Centralized configuration management
- **Files**:
  - `database.py`: Database connection, session management
  - `settings.py`: Application settings, API keys, constants

### 2. **Model Layer** (`app/models/`)
- **Purpose**: Data structures and validation
- **Files**:
  - `auth.py`: User and Session models
  - `schemas.py`: Pydantic schemas for request/response validation

### 3. **Service Layer** (`app/services/`)
- **Purpose**: Business logic and data processing
- **Responsibilities**:
  - Data retrieval and transformation
  - Business rules implementation
  - External API integration (Gemini, Weather, etc.)
- **Files**:
  - `auth_service.py`: Login, logout, token management
  - `sales_service.py`: Sales forecast, metrics calculation
  - `analytics_service.py`: Analytics, inventory predictions
  - `gemini_service.py`: AI insights generation
  - `predictive_service.py`: Predictive analytics with weather/holidays

### 4. **Controller Layer** (`app/controllers/`)
- **Purpose**: Request handling and coordination
- **Responsibilities**:
  - Validate incoming requests
  - Call appropriate services
  - Format responses
- **Files**:
  - `auth_controller.py`: Handle authentication requests
  - `sales_controller.py`: Handle sales-related requests
  - `analytics_controller.py`: Handle analytics requests
  - `settings_controller.py`: Handle settings requests
  - `inventory_controller.py`: Handle inventory requests

### 5. **Route Layer** (`app/routes/`)
- **Purpose**: API endpoint definitions
- **Responsibilities**:
  - Define HTTP routes
  - Map endpoints to controllers
  - Handle dependency injection
- **Files**:
  - `auth_routes.py`: `/login`, `/logout`, `/verify`
  - `sales_routes.py`: `/forecast`, `/sales-data`, `/dashboard-metrics`
  - `analytics_routes.py`: `/sales-analytics`, `/cash-flow`
  - `settings_routes.py`: `/settings/*`
  - `inventory_routes.py`: `/ingredients`, `/products`
  - `ai_routes.py`: `/ai-insights`, `/predictive-insights`

### 6. **Utils Layer** (`app/utils/`)
- **Purpose**: Helper functions and utilities
- **Files**:
  - `model_loader.py`: Load and manage ML models

## Request Flow

```
1. Client Request
   ↓
2. Route (app/routes/)
   - Defines endpoint
   - Applies middleware
   ↓
3. Controller (app/controllers/)
   - Validates request
   - Extracts parameters
   ↓
4. Service (app/services/)
   - Business logic
   - Data processing
   ↓
5. Model (app/models/)
   - Data validation
   - Database interaction
   ↓
6. Response
   - Controller formats response
   - Route returns to client
```

## Example Request Flow

**Example**: User wants to get sales forecast

```python
# 1. Route Definition (routes/sales_routes.py)
@router.get("/forecast")
def forecast(days: int = 7, deps: Dict = Depends(get_dependencies)):
    return SalesController.get_forecast(deps["engine"], deps["sarima_model"], days)

# 2. Controller (controllers/sales_controller.py)
class SalesController:
    @staticmethod
    def get_forecast(engine, sarima_model, days: int = 7):
        return SalesService.get_forecast(engine, days, sarima_model)

# 3. Service (services/sales_service.py)
class SalesService:
    @staticmethod
    def get_forecast(engine, days, sarima_model):
        # Fetch data from database
        # Process with ML model
        # Return forecast
        return forecast_data

# 4. Response sent back to client
```

## Key Features of MVC Implementation

### ✅ **Separation of Concerns**
- Each layer has a specific responsibility
- Business logic separated from request handling
- Easy to test individual components

### ✅ **Dependency Injection**
- Database engine injected via FastAPI dependencies
- ML models loaded once and reused
- Easier testing and mocking

### ✅ **Scalability**
- Easy to add new endpoints
- Simple to extend functionality
- Clear structure for team collaboration

### ✅ **Maintainability**
- Code organized by function
- Easy to locate and fix bugs
- Clear naming conventions

### ✅ **Reusability**
- Services can be reused across controllers
- Models shared between endpoints
- DRY (Don't Repeat Yourself) principle

## Running the Application

### Using the New MVC Structure

1. **Start the server**:
   ```bash
   cd backend
   python -m uvicorn app.main_mvc:app --reload
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Environment Variables Required

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=mysql+pymysql://root:@localhost:3306/databrew

# AI APIs
GEMINI_API_KEY=your_gemini_api_key_here
GROG_API_KEY=your_groq_api_key_here

# Weather API
WEATHER_API_KEY=9CP63WBQHDQ2A52ESSE85KWY4
```

## Migration from Old Structure

### Old Structure (Deprecated)
```
backend/app/
├── main.py                 # 1700+ lines monolithic file
├── auth.py
├── gemini_service.py
├── holiday.py
├── predictive_analytics.py
└── weather_forcast.py
```

### New MVC Structure
- **Models**: Data structures and validation
- **Services**: Business logic (moved from main.py)
- **Controllers**: Request handling (extracted from main.py)
- **Routes**: Endpoint definitions (organized by feature)
- **Config**: Centralized configuration

### Benefits Over Old Structure

| Aspect | Old (Monolithic) | New (MVC) |
|--------|------------------|-----------|
| **File Size** | 1700+ lines in main.py | Max 200 lines per file |
| **Organization** | All in one file | Organized by layer |
| **Testing** | Difficult | Easy to unit test |
| **Collaboration** | Merge conflicts | Multiple devs can work |
| **Maintainability** | Hard to navigate | Clear structure |
| **Scalability** | Limited | Highly scalable |

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - User signup (disabled)
- `POST /logout` - User logout
- `GET /profile` - Get user profile
- `GET /verify` - Verify token

### Sales & Forecasting
- `GET /forecast` - Get sales forecast
- `GET /sales-data` - Get sales trend data
- `GET /dashboard-metrics` - Dashboard metrics
- `GET /best-selling` - Best-selling products

### Analytics & Reporting
- `GET /sales-analytics` - Sales analytics
- `GET /cash-flow` - Cash flow data
- `GET /inventory-predictions` - Inventory predictions
- `GET /barista-schedule` - Staff schedule
- `GET /customer-feedback` - Customer feedback

### AI Insights
- `GET /ai-insights` - AI-generated insights
- `POST /generate-insights` - Generate fresh insights
- `GET /predictive-insights` - Predictive analytics
- `GET /holidays` - Upcoming holidays
- `GET /weather-forecast` - Weather forecast

### Inventory Management
- `GET /ingredients` - Get all ingredients
- `POST /ingredients` - Create ingredient
- `PUT /ingredients/{id}` - Update ingredient
- `DELETE /ingredients/{id}` - Delete ingredient
- `GET /products` - Get all products
- `GET /products/{id}/cost-analysis` - Product cost analysis

### Settings
- `GET /settings/profile` - Get profile settings
- `PUT /settings/profile` - Update profile
- `GET /settings/shop` - Get shop settings
- `PUT /settings/shop` - Update shop settings
- `GET /settings/notifications` - Notification preferences
- `PUT /settings/notifications` - Update notifications
- `POST /settings/change-password` - Change password
- `GET /settings/sessions` - Active sessions

## Testing

### Unit Testing Example

```python
# Test Service Layer
def test_auth_service():
    login_data = LoginRequest(email="admin@gmail.com", password="admin123")
    result = await AuthService.login(login_data)
    assert result.success == True
    assert result.token is not None

# Test Controller
def test_sales_controller(mock_engine):
    result = SalesController.get_forecast(mock_engine, None, days=7)
    assert "forecast_next_days" in result
```

## Best Practices

1. **Always use services for business logic** - Never put business logic in routes or controllers
2. **Keep controllers thin** - Controllers should only coordinate, not contain logic
3. **Use dependency injection** - For database, models, and external services
4. **Follow naming conventions**:
   - Services: `*_service.py`
   - Controllers: `*_controller.py`
   - Routes: `*_routes.py`
5. **One responsibility per file** - Keep files focused on a single concern

## Future Enhancements

- [ ] Add database models using SQLAlchemy ORM
- [ ] Implement comprehensive unit tests
- [ ] Add API rate limiting
- [ ] Implement caching layer (Redis)
- [ ] Add logging middleware
- [ ] Create API versioning (v1, v2)
- [ ] Add WebSocket support for real-time updates
- [ ] Implement background tasks with Celery

## Contributing

When adding new features:

1. **Create service** in `services/` for business logic
2. **Create controller** in `controllers/` for request handling
3. **Define routes** in `routes/` for API endpoints
4. **Add models** in `models/` if needed
5. **Update main_mvc.py** to include new router
6. **Document** in this README

## Questions?

For questions about the MVC architecture, refer to:
- FastAPI documentation: https://fastapi.tiangolo.com/
- MVC pattern: https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
