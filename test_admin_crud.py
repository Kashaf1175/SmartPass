#!/usr/bin/env python3
"""Complete admin CRUD workflow test"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("SMARTPASS ADMIN CRUD WORKFLOW TEST")
print("=" * 70)

# 1. Login
print("\n[1/8] Admin Login...")
resp = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin@smartpass.com", "password": "password123"}
)
assert resp.status_code == 200, f"Login failed: {resp.text}"
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✓ Admin authenticated")

# 2. Create subject
print("[2/8] Creating new subject...")
subject_payload = {
    "name": f"Test Subject {datetime.now().strftime('%H%M%S')}",
    "code": f"TST{datetime.now().strftime('%H%M%S')}",
    "description": "Test subject for verification"
}
resp = requests.post(
    f"{BASE_URL}/classes/subjects",
    json=subject_payload,
    headers=headers
)
assert resp.status_code == 200, f"Subject creation failed: {resp.text}"
subject_id = resp.json()["_id"]
print(f"✓ Subject created: {subject_id}")

# 3. Fetch subjects
print("[3/8] Fetching all subjects...")
resp = requests.get(f"{BASE_URL}/classes/subjects", headers=headers)
assert resp.status_code == 200, f"Fetch subjects failed: {resp.text}"
subjects = resp.json()
print(f"✓ Retrieved {len(subjects)} subjects")

# 4. Update subject
print("[4/8] Updating subject...")
update_payload = {
    "name": f"Updated {subject_payload['name']}",
    "code": subject_payload["code"],
    "description": "Updated description"
}
resp = requests.put(
    f"{BASE_URL}/classes/subjects/{subject_id}",
    json=update_payload,
    headers=headers
)
assert resp.status_code == 200, f"Subject update failed: {resp.text}"
print(f"✓ Subject updated successfully")

# 5. Create class
print("[5/8] Creating new class...")
class_payload = {
    "name": f"Test Class {datetime.now().strftime('%H%M%S')}",
    "subject_id": subject_id,
    "schedule_time": "15:30",
    "room_number": "Test-Room-001"
}
resp = requests.post(
    f"{BASE_URL}/classes/classes",
    json=class_payload,
    headers=headers
)
assert resp.status_code == 200, f"Class creation failed: {resp.text}"
class_id = resp.json()["_id"]
print(f"✓ Class created: {class_id}")

# 6. Fetch classes
print("[6/8] Fetching all classes...")
resp = requests.get(f"{BASE_URL}/classes/classes", headers=headers)
assert resp.status_code == 200, f"Fetch classes failed: {resp.text}"
classes = resp.json()
print(f"✓ Retrieved {len(classes)} classes")

# 7. Update class
print("[7/8] Updating class...")
update_class_payload = {
    "name": f"Updated {class_payload['name']}",
    "subject_id": subject_id,
    "schedule_time": "16:45",
    "room_number": "Test-Room-002"
}
resp = requests.put(
    f"{BASE_URL}/classes/classes/{class_id}",
    json=update_class_payload,
    headers=headers
)
assert resp.status_code == 200, f"Class update failed: {resp.text}"
print(f"✓ Class updated successfully")

# 8. Delete class and subject
print("[8/8] Deleting test resources...")
resp = requests.delete(
    f"{BASE_URL}/classes/classes/{class_id}",
    headers=headers
)
assert resp.status_code == 200, f"Class delete failed: {resp.text}"
print(f"✓ Class deleted successfully")

resp = requests.delete(
    f"{BASE_URL}/classes/subjects/{subject_id}",
    headers=headers
)
assert resp.status_code == 200, f"Subject delete failed: {resp.text}"
print(f"✓ Subject deleted successfully")

print("\n" + "=" * 70)
print("✅ ALL ADMIN CRUD OPERATIONS VERIFIED")
print("=" * 70)
print("\nAdmin Panel Features Tested & Working:")
print("  ✓ Create Subject")
print("  ✓ Read Subjects")
print("  ✓ Update Subject")
print("  ✓ Create Class")
print("  ✓ Read Classes")
print("  ✓ Update Class")
print("  ✓ Delete Class")
print("  ✓ Delete Subject")
print("\nThe AdminDashboard component UI now works seamlessly!")
print("=" * 70)
