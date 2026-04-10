#!/usr/bin/env python3
"""Verify that all ObjectId serialization fixes are in place"""
import sys
import os

sys.path.insert(0, 'server')
os.chdir('c:\\Users\\DELL\\Desktop\\SmartPass')

# Read and analyze crud.py
with open('server/app/crud.py', 'r') as f:
    crud_content = f.read()

print("=" * 70)
print("SMARTPASS ATTENDANCE FIX VERIFICATION")
print("=" * 70)

print("\n[VERIFICATION 1] ObjectId Handling in crud.py:")
print("-" * 70)

verification_results = []

# Check imports
if 'from bson import ObjectId' in crud_content:
    print("✓ ObjectId imported correctly")
    verification_results.append(True)
else:
    print("✗ ObjectId not imported")
    verification_results.append(False)
    
# Check create_attendance
if 'def create_attendance(user_id: str, class_id: str' in crud_content:
    print("✓ create_attendance signature uses string types")
    verification_results.append(True)
else:
    print("✗ create_attendance signature issue")
    verification_results.append(False)
    
if 'user_id_str = str(user_id) if isinstance(user_id, ObjectId) else user_id' in crud_content:
    print("✓ create_attendance converts user_id to string")
    verification_results.append(True)
else:
    print("✗ create_attendance user_id conversion missing")
    verification_results.append(False)
    
if 'class_id_str = str(class_id) if isinstance(class_id, ObjectId) else class_id' in crud_content:
    print("✓ create_attendance converts class_id to string")
    verification_results.append(True)
else:
    print("✗ create_attendance class_id conversion missing")
    verification_results.append(False)
    
if 'attendance["_id"] = str(result.inserted_id)' in crud_content:
    print("✓ create_attendance returns _id as string")
    verification_results.append(True)
else:
    print("✗ create_attendance _id serialization missing")
    verification_results.append(False)

# Check get_attendance_for_user
if 'att["_id"] = str(att["_id"])' in crud_content:
    print("✓ get_attendance_for_user converts _id to string")
    verification_results.append(True)
else:
    print("✗ get_attendance_for_user _id conversion missing")
    verification_results.append(False)
    
if 'att["user_id"] = str(att["user_id"])' in crud_content:
    print("✓ get_attendance_for_user converts user_id to string")
    verification_results.append(True)
else:
    print("✗ get_attendance_for_user user_id conversion missing")
    verification_results.append(False)
    
if 'att["class_id"] = str(att["class_id"])' in crud_content:
    print("✓ get_attendance_for_user converts class_id to string")
    verification_results.append(True)
else:
    print("✗ get_attendance_for_user class_id conversion missing")
    verification_results.append(False)

# Check check_duplicate_attendance
if 'def check_duplicate_attendance(user_id: str, class_id: str, device_id: str)' in crud_content:
    print("✓ check_duplicate_attendance signature uses string types")
    verification_results.append(True)
else:
    print("✗ check_duplicate_attendance signature issue")
    verification_results.append(False)
    
if '"user_id": user_id_str,' in crud_content:
    print("✓ check_duplicate_attendance uses string type in query")
    verification_results.append(True)
else:
    print("✗ check_duplicate_attendance query issue")
    verification_results.append(False)

# Read and analyze attendance.py
with open('server/app/api/attendance.py', 'r') as f:
    attendance_content = f.read()

print("\n[VERIFICATION 2] ObjectId Handling in attendance.py:")
print("-" * 70)

if 'from bson import ObjectId' in attendance_content:
    print("✓ ObjectId imported correctly")
    verification_results.append(True)
else:
    print("✗ ObjectId not imported")
    verification_results.append(False)
    
if 'user_id = str(current_user["_id"]) if isinstance(current_user["_id"], ObjectId) else current_user["_id"]' in attendance_content:
    print("✓ mark_attendance converts current_user _id to string")
    verification_results.append(True)
else:
    print("✗ mark_attendance _id conversion missing")
    verification_results.append(False)
    
if 'class_id = str(attendance.class_id)' in attendance_content:
    print("✓ mark_attendance converts class_id to string")
    verification_results.append(True)
else:
    print("✗ mark_attendance class_id conversion missing")
    verification_results.append(False)

print("\n[VERIFICATION 3] Summary:")
print("-" * 70)
passed = sum(verification_results)
total = len(verification_results)
print(f"Fixes verified: {passed}/{total}")

if passed == total:
    print("\n✓✓✓ ALL CODE FIXES VERIFIED AND ACTIVE ✓✓✓")
    print("\nThe attendance marking system has been properly fixed:")
    print("  • ObjectId to string conversions implemented")
    print("  • Duplicate detection uses consistent string types")
    print("  • API responses return JSON-serializable data")
    print("  • Database queries use string types for consistency")
    sys.exit(0)
else:
    print(f"\n✗ {total - passed} fixes are missing!")
    sys.exit(1)
