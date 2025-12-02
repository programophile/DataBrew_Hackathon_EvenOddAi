"""
Application settings and configuration
"""
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Settings
APP_NAME = "Coffee Sales Analytics API"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Fixed current date for the application (2023-06-24)
CURRENT_DATE = datetime(2023, 6, 24)

# CORS Settings
CORS_ORIGINS = ["*"]  # Change to specific domains in production

# Authentication Settings
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"
TOKEN_EXPIRY_DAYS = 7

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROG_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "9CP63WBQHDQ2A52ESSE85KWY4")

# Location Settings (Dhaka, Bangladesh)
LATITUDE = 23.7918
LONGITUDE = 90.3943

# Holiday API Settings
HOLIDAYS_API_URL = "https://date.nager.at/api/v3/PublicHolidays"
DEFAULT_COUNTRY_CODE = "BD"

# Model Paths
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
SARIMA_MODEL_PATH = os.path.join(MODELS_DIR, "sarima_model_forcast.pkl")

# Database Settings
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/databrew")
