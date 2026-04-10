import pandas as pd
import numpy as np
from typing import List, Tuple
from datetime import datetime

def prepare_features(attendance_records) -> pd.DataFrame:
    """Convert attendance records to feature DataFrame for ML"""
    data = []
    for record in attendance_records:
        ts = record.timestamp or record.created_at
        data.append({
            "hour": ts.hour,
            "latitude": record.latitude or 0.0,
            "longitude": record.longitude or 0.0,
            "device_code": _device_code(record.device_id),
        })

    return pd.DataFrame(data)

def _device_code(device_id: str) -> int:
    """Convert device ID to numeric code"""
    return abs(hash(device_id or "unknown")) % 1000

def calculate_fraud_score(features: np.ndarray, model) -> Tuple[int, bool]:
    """Calculate fraud score from model prediction"""
    if model is None:
        return 0, False

    try:
        score = float(model.decision_function(features)[0])
        # Convert to 0-100 scale (lower score = more anomalous)
        normalized = np.clip((0.35 - score) / 0.7, 0, 1)
        fraud_score = int(normalized * 100)
        is_flagged = fraud_score >= 65
        return fraud_score, is_flagged
    except Exception:
        return 0, False

def generate_synthetic_data(n_samples: int = 100) -> pd.DataFrame:
    """Generate synthetic attendance data for testing"""
    np.random.seed(42)

    data = []
    for i in range(n_samples):
        # Normal distribution around typical attendance times
        hour = np.random.normal(9, 2)  # Mean 9 AM, std dev 2 hours
        hour = max(0, min(23, int(hour)))

        # Normal location (e.g., campus)
        lat = np.random.normal(37.42, 0.01)
        lon = np.random.normal(-122.08, 0.01)

        # Device consistency
        device_code = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])

        # Introduce some anomalies
        if np.random.random() < 0.1:  # 10% anomalous
            hour = np.random.choice([2, 3, 22, 23])  # Unusual hours
            lat = np.random.normal(40.71, 0.1)  # Different city
            lon = np.random.normal(-74.00, 0.1)
            device_code = np.random.randint(100, 200)  # Different device

        data.append({
            "hour": hour,
            "latitude": lat,
            "longitude": lon,
            "device_code": device_code,
        })

    return pd.DataFrame(data)

def evaluate_model_performance(model, X_test, y_test) -> dict:
    """Evaluate model performance metrics"""
    from sklearn.metrics import classification_report, confusion_matrix

    predictions = model.predict(X_test)
    scores = model.decision_function(X_test)

    return {
        "classification_report": classification_report(y_test, predictions, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "anomaly_scores": scores.tolist(),
    }