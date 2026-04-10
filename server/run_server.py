#!/usr/bin/env python3
"""Simple startup script for SmartPass backend"""
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'app'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

# Import our modules directly
from api import auth, attendance, fraud, classes
from core.config import ALLOWED_ORIGINS

app = FastAPI(
    title="Smart Attendance Fraud Detection System",
    description="Detect suspicious attendance behavior in real time.",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$|https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
app.include_router(fraud.router, prefix="/fraud", tags=["fraud"])
app.include_router(classes.router, prefix="/classes", tags=["classes"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "SmartPass backend is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)