#!/usr/bin/env python3
"""Test SmartPass API endpoints end-to-end"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
TOKEN = None

def test_login():
    """Test admin authentication"""
    global TOKEN
    print("\n=== Step 1: Testing Admin Authentication ===")
    try:
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": "admin@smartpass.com", "password": "password123"},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            TOKEN = data["access_token"]
            print(f"✓ Admin login successful")
            print(f"  Email: admin@smartpass.com | Token received")
            return True
        else:
            print(f"✗ Login failed: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"✗ Login error: {e}")
        return False

def test_subjects():
    """Test fetching subjects"""
    print("\n=== Step 2: Fetching Subjects ===")
    try:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        resp = requests.get(f"{BASE_URL}/classes/subjects", headers=headers, timeout=5)
        if resp.status_code == 200:
            subjects = resp.json()
            print(f"✓ Retrieved {len(subjects)} subjects")
            if subjects:
                first_subj = subjects[0]
                print(f"  Sample: {first_subj.get('name', 'N/A')} ({first_subj.get('code', 'N/A')})")
            return True
        else:
            print(f"✗ Fetch subjects failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Subjects error: {e}")
        return False

def test_classes():
    """Test fetching classes"""
    print("\n=== Step 3: Fetching Classes ===")
    try:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        resp = requests.get(f"{BASE_URL}/classes/classes", headers=headers, timeout=5)
        if resp.status_code == 200:
            classes = resp.json()
            print(f"✓ Retrieved {len(classes)} classes")
            if classes:
                first_cls = classes[0]
                print(f"  Sample: {first_cls.get('name', 'N/A')} (Schedule: {first_cls.get('schedule_time', 'N/A')})")
            return True
        else:
            print(f"✗ Fetch classes failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Classes error: {e}")
        return False

def test_student_login():
    """Test student authentication"""
    print("\n=== Step 4: Testing Student Authentication ===")
    try:
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": "student1@smartpass.com", "password": "password123"},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ Student login successful")
            print(f"  Email: student1@smartpass.com | Token received")
            return True
        else:
            print(f"✗ Student login failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Student login error: {e}")
        return False

def test_fraud_analysis():
    """Test fraud analysis endpoint"""
    print("\n=== Step 5: Fetching Fraud Analysis ===")
    try:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        resp = requests.get(f"{BASE_URL}/fraud/fraud-stats", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ Fraud analysis retrieved")
            print(f"  Total records: {data.get('total_records', 0)} | Flagged: {len(data.get('flagged', []))}")
            return True
        else:
            print(f"✗ Fraud analysis failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Fraud analysis error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SmartPass API End-to-End Test")
    print("=" * 60)
    
    results = []
    results.append(("Authentication", test_login()))
    
    if TOKEN:
        results.append(("Subjects", test_subjects()))
        results.append(("Classes", test_classes()))
        results.append(("Fraud Analysis", test_fraud_analysis()))
    
    results.append(("Student Auth", test_student_login()))
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<40} {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("=" * 60))
    if all_passed:
        print("✓ ALL TESTS PASSED - System is fully operational!")
        print("\nAccess the application:")
        print("  Frontend: http://localhost:5175")
        print("  Backend Docs: http://localhost:8000/docs")
    else:
        print("✗ Some tests failed - Check output above")
    print("=" * 60)
