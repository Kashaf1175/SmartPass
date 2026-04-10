import os
import sys
from pathlib import Path

# Add the server app to the path
sys.path.append(str(Path(__file__).parent.parent / "server"))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.attendance import Attendance
from predict import train_model

def seed_training_data(db: Session):
    """Create synthetic training data if database is empty"""
    if db.query(Attendance).count() < 10:
        print("Creating synthetic training data...")

        # Create a test user if none exists
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            from app.core.security import get_password_hash
            test_user = User(
                email="test@example.com",
                hashed_password=get_password_hash("password"),
                role="student"
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)

        # Create synthetic attendance records
        import random
        from datetime import datetime, timedelta

        for i in range(50):
            # Normal attendance patterns
            hour = 8 + (i % 4)  # 8-11 AM
            lat = 37.42 + (random.random() - 0.5) * 0.01
            lon = -122.08 + (random.random() - 0.5) * 0.01
            device = f"device-{(i % 3) + 1}"

            # Some anomalous records
            if i % 10 == 0:  # Every 10th record is anomalous
                hour = random.choice([2, 23])  # Unusual hours
                lat = 40.71  # Different location (NYC)
                lon = -74.00
                device = f"suspicious-device-{i}"

            attendance = Attendance(
                user_id=test_user.id,
                timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                latitude=lat,
                longitude=lon,
                device_id=device,
                ip_address="127.0.0.1",
                fraud_score=0,  # Will be calculated by ML model
                is_flagged=False
            )
            db.add(attendance)

        db.commit()
        print("Synthetic training data created.")

def main():
    """Train the ML model"""
    print("Training fraud detection model...")

    db = SessionLocal()
    try:
        # Seed data if needed
        seed_training_data(db)

        # Train the model
        model = train_model(db)
        print("Model trained successfully!")

    except Exception as e:
        print(f"Error training model: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()