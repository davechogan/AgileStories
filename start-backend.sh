#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Navigate to backend directory
cd backend

# Start the FastAPI server
uvicorn app.main:app --reload