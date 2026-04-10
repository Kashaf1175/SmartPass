from typing import Optional
from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format datetime for API responses"""
    return dt.isoformat()

def validate_coordinates(latitude: Optional[float], longitude: Optional[float]) -> bool:
    """Validate latitude and longitude values"""
    if latitude is None or longitude is None:
        return False
    return -90 <= latitude <= 90 and -180 <= longitude <= 180

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula"""
    from math import radians, cos, sin, asin, sqrt

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def normalize_fraud_score(score: float) -> int:
    """Normalize fraud score to 0-100 range"""
    return max(0, min(100, int(score * 100)))

def is_suspicious_time(hour: int) -> bool:
    """Check if attendance time is suspicious (outside normal hours)"""
    return hour < 6 or hour > 22  # Outside 6 AM - 10 PM