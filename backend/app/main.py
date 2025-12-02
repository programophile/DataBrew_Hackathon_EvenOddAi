from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import crud
from app.schemas import WeeklySalesSummary
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coffee Shop Analytics API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/sales/weekly-summary", response_model=WeeklySalesSummary)
def weekly_sales_report(db: Session = Depends(get_db)):
    summary = crud.get_top_increase_decrease(db)
    return summary