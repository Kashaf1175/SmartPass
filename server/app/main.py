from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, attendance, fraud, classes
from .core.config import ALLOWED_ORIGINS

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

@app.get("/")
def root():
    return {"message": "Smart Attendance Fraud Detection API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/debug/database")
def debug_database():
    """Debug endpoint to check database connectivity"""
    try:
        from .core.database import db
        classes_count = db.classes.count_documents({})
        subjects_count = db.subjects.count_documents({})
        users_count = db.users.count_documents({})
        return {
            "status": "connected",
            "database": db.name,
            "collections": {
                "classes": classes_count,
                "subjects": subjects_count,
                "users": users_count
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

import traceback