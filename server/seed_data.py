#!/usr/bin/env python3
"""
Seed script to populate the SmartPass database with sample data.
Run this script to add sample subjects, classes, and users for testing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import db
from app.crud import create_subject, create_class, create_user
from app.core.security import get_password_hash

def seed_database():
    print("🌱 Seeding SmartPass database...")

    # Clear existing data
    print("🧹 Clearing existing data...")
    db.subjects.delete_many({})
    db.classes.delete_many({})
    db.users.delete_many({})
    db.attendances.delete_many({})

    # Create sample subjects
    print("📚 Creating subjects...")
    subjects_data = [
        {"name": "Computer Science", "code": "CS101", "description": "Introduction to Computer Science"},
        {"name": "Mathematics", "code": "MATH101", "description": "Calculus and Algebra"},
        {"name": "Physics", "code": "PHYS101", "description": "Classical Physics"},
        {"name": "Chemistry", "code": "CHEM101", "description": "Organic Chemistry"},
        {"name": "Biology", "code": "BIO101", "description": "Molecular Biology"},
    ]

    subjects = []
    for subject_data in subjects_data:
        subject = create_subject(subject_data)
        subjects.append(subject)
        print(f"  ✓ Created subject: {subject['name']} ({subject['code']})")

    # Create sample classes
    print("🏫 Creating classes...")
    classes_data = [
        {"name": "CS101 - Lecture A", "subject_id": subjects[0]["_id"], "schedule_time": "09:00:00", "room_number": "Room 101"},
        {"name": "CS101 - Lab A", "subject_id": subjects[0]["_id"], "schedule_time": "14:00:00", "room_number": "Lab 201"},
        {"name": "MATH101 - Lecture B", "subject_id": subjects[1]["_id"], "schedule_time": "10:00:00", "room_number": "Room 102"},
        {"name": "PHYS101 - Lecture C", "subject_id": subjects[2]["_id"], "schedule_time": "11:00:00", "room_number": "Room 103"},
        {"name": "CHEM101 - Lab B", "subject_id": subjects[3]["_id"], "schedule_time": "15:00:00", "room_number": "Lab 202"},
        {"name": "BIO101 - Lecture D", "subject_id": subjects[4]["_id"], "schedule_time": "13:00:00", "room_number": "Room 104"},
    ]

    classes = []
    for class_data in classes_data:
        class_obj = create_class(class_data)
        classes.append(class_obj)
        print(f"  ✓ Created class: {class_obj['name']}")

    # Create sample users
    print("👥 Creating users...")
    users_data = [
        {"email": "admin@smartpass.com", "role": "admin"},
        {"email": "student1@smartpass.com", "role": "student"},
        {"email": "student2@smartpass.com", "role": "student"},
        {"email": "student3@smartpass.com", "role": "student"},
        {"email": "student4@smartpass.com", "role": "student"},
        {"email": "student5@smartpass.com", "role": "student"},
    ]

    for user_data in users_data:
        hashed_password = get_password_hash("password123")
        user = create_user(user_data, hashed_password)
        print(f"  ✓ Created user: {user['email']} ({user['role']})")

    print("\n✅ Database seeded successfully!")
    print("\n📋 Sample login credentials:")
    print("Admin: admin@smartpass.com / password123")
    print("Students: student1@smartpass.com - student5@smartpass.com / password123")
    print("\n📚 Available subjects and classes are now ready for testing!")

if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        sys.exit(1)