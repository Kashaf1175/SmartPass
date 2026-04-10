from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from .core.config import CAMPUS_LATITUDE, CAMPUS_LONGITUDE, CAMPUS_RADIUS_KM, FRAUD_THRESHOLD

UNUSUAL_HOURS = set(range(0, 6)) | set(range(20, 24))


def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 1000.0  # Large distance if coordinates missing
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371.0 * c


def _time_score(timestamp: datetime) -> int:
    if not isinstance(timestamp, datetime):
        return 0
    if timestamp.hour in UNUSUAL_HOURS:
        return 40
    return 0


def _location_score(latitude: float | None, longitude: float | None) -> int:
    distance = _haversine_distance(latitude, longitude, CAMPUS_LATITUDE, CAMPUS_LONGITUDE)
    if distance > CAMPUS_RADIUS_KM:
        return 50  # Outside campus
    return 0


def is_within_campus(latitude: float | None, longitude: float | None) -> bool:
    if latitude is None or longitude is None:
        return False
    distance = _haversine_distance(latitude, longitude, CAMPUS_LATITUDE, CAMPUS_LONGITUDE)
    return distance <= CAMPUS_RADIUS_KM


def _device_score(device_id: str) -> int:
    if not device_id:
        return 10
    return 0


def _analyze_user_behavior(db, user_id: str, timestamp, latitude, longitude, device_id):
    """Analyze user behavior patterns"""
    score = 0
    reasons = []
    
    # Get user's historical attendance
    historical = list(db.attendances.find({"user_id": user_id}).sort("timestamp", -1).limit(50))
    
    if not historical:
        return 0, []  # New user, no behavior to analyze
    
    # Check device consistency
    user_devices = set(att['device_id'] for att in historical if att.get('device_id'))
    if device_id and device_id not in user_devices:
        score += 20
        reasons.append("new device")
    
    # Check time pattern
    user_hours = [att['timestamp'].hour for att in historical]
    current_hour = timestamp.hour
    if user_hours:
        avg_hour = sum(user_hours) / len(user_hours)
        if abs(current_hour - avg_hour) > 2:  # More than 2 hours from average
            score += 15
            reasons.append("unusual login time")
    
    # Check location clusters (simplified)
    user_locations = [(att.get('latitude'), att.get('longitude')) for att in historical 
                     if att.get('latitude') and att.get('longitude')]
    if user_locations and latitude and longitude:
        # Check if current location is within user's typical area
        distances = [_haversine_distance(lat, lon, latitude, longitude) for lat, lon in user_locations]
        min_distance = min(distances)
        if min_distance > 1.0:  # More than 1km from any previous location
            score += 25
            reasons.append("unusual location")
    
    return score, reasons


def analyze_attendance(db, user_id: str, timestamp, latitude, longitude, device_id):
    time_score = _time_score(timestamp)
    location_score = _location_score(latitude, longitude)
    device_score = _device_score(device_id)
    
    # User behavior profiling
    behavior_score, behavior_reasons = _analyze_user_behavior(db, user_id, timestamp, latitude, longitude, device_id)
    
    fraud_score = min(100, time_score + location_score + device_score + behavior_score)
    
    reasons = []
    if time_score > 0:
        reasons.append("unusual time")
    if location_score > 0:
        reasons.append("outside campus")
    if device_score > 0:
        reasons.append("missing device info")
    reasons.extend(behavior_reasons)
    
    return fraud_score, fraud_score >= FRAUD_THRESHOLD, reasons


def train_model(db):
    # Placeholder for model training. This backend uses a simple heuristic model.
    return None
