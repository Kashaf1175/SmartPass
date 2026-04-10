#!/usr/bin/env python3
"""
Database migration script to create or update database schema.
"""

import sys
from pathlib import Path

# Add the server app to the path
sys.path.append(str(Path(__file__).parent.parent / "server"))

from sqlalchemy import create_engine
from app.core.database import Base, engine
from app.models.user import User
from app.models.attendance import Attendance

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def drop_tables():
    """Drop all database tables (use with caution!)"""
    print("Dropping database tables...")
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")

def reset_database():
    """Reset database by dropping and recreating all tables"""
    print("Resetting database...")
    drop_tables()
    create_tables()
    print("Database reset completed!")

def main():
    """Main migration function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "create":
            create_tables()
        elif command == "drop":
            drop_tables()
        elif command == "reset":
            reset_database()
        else:
            print("Usage: python run_migrations.py [create|drop|reset]")
            print("  create: Create all database tables")
            print("  drop: Drop all database tables")
            print("  reset: Drop and recreate all database tables")
    else:
        # Default action: create tables
        create_tables()

if __name__ == "__main__":
    main()