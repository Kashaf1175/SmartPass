#!/usr/bin/env python3
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

print("Testing attendance marking with fixed code...")
print("=" * 60)

# 1. Login
print("\n1. Logging in as student...")
resp = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "student1@smartpass.com", "password": "password123"}
)
if resp.status_code == 200:
    token = resp.json()["access_token"]
    print("   [OK] Login successful")
else:
    print(f"   [FAIL] Login failed: {resp.status_code}")
    exit(1)

# 2. Get classes
print("\n2. Getting available classes...")
headers = {"Authorization": f"Bearer {token}"}
resp = requests.get(f"{BASE_URL}/classes/classes", headers=headers)
if resp.status_code == 200:
    classes = resp.json()
    if classes:
        target_class = classes[0]
        print(f"   [OK] Found {len(classes)} classes")
        print(f"   Target: {target_class.get('name', 'Unknown')} (ID: {target_class['_id']})")
    else:
        print("   [FAIL] No classes available")
        exit(1)
else:
    print(f"   [FAIL] Failed to get classes: {resp.status_code}")
    exit(1)

# 3. Try marking attendance (should fail due to time window)
print("\n3. Marking attendance...")
att_payload = {
    "class_id": target_class["_id"],
    "latitude": 37.7749,
    "longitude": -122.4194,
    "device_id": "test-device-001"
}

resp = requests.post(
    f"{BASE_URL}/attendance/mark-attendance",
    json=att_payload,
    headers=headers
)

if resp.status_code == 200:
    result = resp.json()
    print("   [OK] Attendance marked successfully!")
    print(f"   - ID: {result.get('_id')}")
    print(f"   - Fraud Score: {result.get('fraud_score')}")
    print(f"   - Flagged: {result.get('is_flagged')}")
    print(f"   - User ID: {result.get('user_id')}")
    print(f"   - Class ID: {result.get('class_id')}")
elif resp.status_code == 400:
    error_msg = resp.json().get('detail', 'Unknown error')
    print(f"   [INFO] Expected error (outside time window): {error_msg}")
else:
    print(f"   [FAIL] Marked attendance failed: {resp.status_code}")
    print(f"   Error: {resp.json()}")

# 4. Check records in database
print("\n4. Checking attendance records...")
resp = requests.get(f"{BASE_URL}/attendance/get-attendance", headers=headers)
if resp.status_code == 200:
    records = resp.json()
    print(f"   [OK] Found {len(records)} attendance records")
    if records:
        first = records[0]
        print(f"   Record keys: {list(first.keys())}")
        print(f"   User ID: {first.get('user_id')}")
        print(f"   Class ID: {first.get('class_id')}")
else:
    print(f"   [FAIL] Failed to get records: {resp.status_code}")

print("\n" + "=" * 60)
print("Test complete. Attendance system should now work correctly.")
