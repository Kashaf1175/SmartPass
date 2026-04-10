import os
from typing import List


def _parse_csv_env(var_name: str) -> List[str]:
    value = os.getenv(var_name, "").strip()
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

# Database
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "smartpass")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "smartpass-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# CORS
DEFAULT_ALLOWED_ORIGINS: List[str] = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:5177",
    "http://localhost:5178",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:5176",
    "http://127.0.0.1:5177",
    "http://127.0.0.1:5178",
    "http://localhost:3000",
    "http://localhost:8080",
]
ALLOWED_ORIGINS: List[str] = _parse_csv_env("ALLOWED_ORIGINS") or DEFAULT_ALLOWED_ORIGINS

# ML Model
MODEL_PATH = "app/ml_model.joblib"
MIN_TRAINING_SAMPLES = 20
FRAUD_THRESHOLD = 65

# Campus Geo-Fencing
# Default: SGGSIE&T, Vishnupuri, Nanded
CAMPUS_LATITUDE = float(os.getenv("CAMPUS_LATITUDE", "19.1116656"))
CAMPUS_LONGITUDE = float(os.getenv("CAMPUS_LONGITUDE", "77.2929891"))
CAMPUS_RADIUS_KM = float(os.getenv("CAMPUS_RADIUS_KM", "1.5"))

# Email Alerts
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@college.edu")