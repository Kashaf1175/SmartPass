#!/usr/bin/env python3
import sys
sys.path.append('c:\\Users\\DELL\\Desktop\\SmartPass\\server')

from app.core.database import db

# Clear attendances collection to reset with correct types
db.attendances.delete_many({})
count = db.attendances.count_documents({})
print(f"Attendances collection cleared. Current count: {count}")
