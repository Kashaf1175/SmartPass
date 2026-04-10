#!/usr/bin/env python3
"""
Seed script to populate the database with initial data for testing.
"""

import sys
from pathlib import Path

# Add the server app to the path
sys.path.append(str(Path(__file__).parent.parent / "server"))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.attendance import Attendance
from app.models.subject import Subject
from app.models.class_model import Class
from app.core.security import get_password_hash
from datetime import datetime, timedelta, time
import random

def create_admin_user(db: Session):
    """Create admin user"""
    admin = db.query(User).filter(User.email == "admin@smartpass.com").first()
    if not admin:
        admin = User(
            email="admin@smartpass.com",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("Admin user created: admin@smartpass.com / admin123")
    return admin

def create_student_users(db: Session, count: int = 5):
    """Create sample student users"""
    students = []
    for i in range(count):
        email = f"student{i+1}@smartpass.com"
        student = db.query(User).filter(User.email == email).first()
        if not student:
            student = User(
                email=email,
                hashed_password=get_password_hash("password123"),
                role="student"
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            students.append(student)
            print(f"Student user created: {email} / password123")
    return students

def create_subjects(db: Session):
    """Create sample subjects"""
    subjects_data = [
        {"name": "Mathematics", "code": "MATH101"},
        {"name": "Physics", "code": "PHY101"},
        {"name": "Chemistry", "code": "CHEM101"},
        {"name": "English", "code": "ENG101"},
        {"name": "Computer Science", "code": "CS101"},
    ]
    
    subjects = []
    for subj_data in subjects_data:
        subject = db.query(Subject).filter(Subject.code == subj_data["code"]).first()
        if not subject:
            subject = Subject(name=subj_data["name"], code=subj_data["code"])
            db.add(subject)
            db.commit()
            db.refresh(subject)
            subjects.append(subject)
            print(f"Subject created: {subj_data['name']} ({subj_data['code']})")
    return subjects

def create_classes(db: Session, subjects: list):
    """Create sample classes for subjects"""
    for subject in subjects:
        for i in range(2):  # 2 classes per subject
            class_name = f"{subject.name} - Class {i+1}"
            class_time = time(8 + i, 0)  # 8 AM and 9 AM
            
            existing_class = db.query(Class).filter(
                Class.subject_id == subject.id,
                Class.name == class_name
            ).first()
            
            if not existing_class:
                new_class = Class(
                    name=class_name,
                    subject_id=subject.id,
                    schedule_time=class_time,
                    room_number=f"Room {100 + subject.id}{i+1}"
                )
                db.add(new_class)
                db.commit()
                db.refresh(new_class)
                print(f"Class created: {class_name} at {class_time} ({subject.id})")

def create_attendance_records(db: Session, students: list, classes: list, records_per_student: int = 5):
    """Create sample attendance records with class references"""
    for student in students:
        for i in range(records_per_student):
            # Select a random class
            selected_class = random.choice(classes)
            
            # Create records over the past 30 days
            days_ago = random.randint(0, 30)
            timestamp = datetime.utcnow() - timedelta(days=days_ago)

            # Normal attendance patterns
            lat = 37.42 + (random.random() - 0.5) * 0.02  # Near campus
            lon = -122.08 + (random.random() - 0.5) * 0.02
            device = f"device-{student.id}"

            # Some anomalous records
            if random.random() < 0.15:  # 15% anomalous
                if random.random() < 0.5:
                    lat = 40.71 + (random.random() - 0.5) * 0.1  # Different city
                    lon = -74.00 + (random.random() - 0.5) * 0.1
                else:
                    device = f"suspicious-device-{random.randint(100, 999)}"

            attendance = Attendance(
                user_id=student.id,
                class_id=selected_class.id,
                timestamp=timestamp,
                latitude=lat,
                longitude=lon,
                device_id=device,
                ip_address=f"192.168.1.{random.randint(1, 255)}",
                fraud_score=0,  # Will be calculated by ML model
                is_flagged=False
            )
            db.add(attendance)

    db.commit()
    print(f"Created attendance records for {len(students)} students across {len(classes)} classes")

def main():
    """Main seeding function"""
    print("Seeding database with initial data...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Create users
        admin = create_admin_user(db)
        students = create_student_users(db)

        # Create subjects and classes
        subjects = create_subjects(db)
        # Get all classes that were created
        all_classes = db.query(Class).all()
        create_classes(db, subjects)
        all_classes = db.query(Class).all()

        # Create attendance records
        create_attendance_records(db, students, all_classes)

        print("Database seeding completed successfully!")
        print("\nTest accounts:")
        print("Admin: admin@smartpass.com / admin123")
        print("Students: student1@smartpass.com - student5@smartpass.com / password123")
        print(f"\nCreated {len(subjects)} subjects and {len(all_classes)} classes")

    except Exception as e:
        print(f"Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()