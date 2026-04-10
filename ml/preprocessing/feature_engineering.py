import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta

def extract_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract time-based features from attendance data"""
    df = df.copy()

    # Time of day categories
    df['time_category'] = pd.cut(df['hour'],
                                bins=[0, 6, 12, 18, 24],
                                labels=['night', 'morning', 'afternoon', 'evening'])

    # Is weekend
    df['is_weekend'] = df['timestamp'].dt.dayofweek >= 5

    # Is business hours
    df['is_business_hours'] = (df['hour'] >= 8) & (df['hour'] <= 18)

    return df

def extract_location_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract location-based features"""
    df = df.copy()

    # Calculate distance from expected location (assuming campus center)
    campus_lat, campus_lon = 37.42, -122.08
    df['distance_from_campus'] = calculate_distance(
        df['latitude'], df['longitude'], campus_lat, campus_lon
    )

    # Location clusters (simplified)
    df['location_cluster'] = pd.cut(df['distance_from_campus'],
                                   bins=[0, 0.1, 1, 10, 1000],
                                   labels=['on_campus', 'near_campus', 'city', 'far'])

    return df

def extract_device_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract device-related features"""
    df = df.copy()

    # Device frequency
    device_counts = df.groupby('device_code').size()
    df['device_frequency'] = df['device_code'].map(device_counts)

    # Device changes over time (simplified)
    df = df.sort_values('timestamp')
    df['device_changed'] = df.groupby('user_id')['device_code'].diff() != 0

    return df

def extract_user_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Extract user behavior patterns"""
    df = df.copy()

    # Rolling statistics for each user
    for user_id in df['user_id'].unique():
        user_data = df[df['user_id'] == user_id].copy()
        user_data = user_data.sort_values('timestamp')

        # Rolling mean of hours (last 5 attendances)
        user_data['hour_rolling_mean'] = user_data['hour'].rolling(5).mean()
        user_data['hour_rolling_std'] = user_data['hour'].rolling(5).std()

        # Update main dataframe
        for idx in user_data.index:
            df.loc[idx, 'hour_rolling_mean'] = user_data.loc[idx, 'hour_rolling_mean']
            df.loc[idx, 'hour_rolling_std'] = user_data.loc[idx, 'hour_rolling_std']

    return df

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

def create_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Create final feature matrix for ML model"""
    # Start with basic features
    features = df[['hour', 'latitude', 'longitude', 'device_code']].copy()

    # Add engineered features
    features['distance_from_campus'] = calculate_distance(
        df['latitude'], df['longitude'], 37.42, -122.08
    )

    # Time-based features
    features['is_business_hours'] = ((df['hour'] >= 8) & (df['hour'] <= 18)).astype(int)
    features['is_weekend'] = (df['timestamp'].dt.dayofweek >= 5).astype(int)

    # Device features
    device_counts = df.groupby('device_code').size()
    features['device_frequency'] = df['device_code'].map(device_counts)

    # Fill NaN values
    features = features.fillna(0)

    return features