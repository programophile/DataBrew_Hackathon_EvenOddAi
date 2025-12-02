"""
Database configuration module
Handles database connection setup
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - using MySQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/databrew")

# Create database engine
engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    """Initialize database connection"""
    global engine, SessionLocal

    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("✓ Database connection established successfully")
        return engine
    except Exception as e:
        print(f"Warning: Could not create database engine: {e}")
        return None

def get_db():
    """
    Dependency function to get database session
    Yields a database session and closes it after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    """Get database engine instance"""
    global engine
    if engine is None:
        engine = init_db()
    return engine
