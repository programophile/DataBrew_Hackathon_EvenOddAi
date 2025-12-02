#!/bin/bash
echo "Starting DataBrew Backend Server..."
cd backend
source venv/bin/activate
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
