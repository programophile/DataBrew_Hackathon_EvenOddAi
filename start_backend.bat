@echo off
echo Starting DataBrew Backend Server...
cd backend
call venv\Scripts\activate
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
