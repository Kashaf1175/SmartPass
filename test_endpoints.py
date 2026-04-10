#!/usr/bin/env python3
import requests

# Login first
resp = requests.post('http://localhost:8000/auth/login', 
                    data={'username': 'admin@smartpass.com', 'password': 'password123'})
                    
if resp.status_code != 200:
    print(f"Login failed: {resp.status_code}")
    exit(1)

token = resp.json()['access_token']
print(f"✓ Logged in. Token: {token[:20]}...")

# Test different endpoints
endpoints = [
    '/classes',
    '/classes/classes',
    '/classes/subjects',
    '/fraud/analysis',
    '/fraud/fraud-stats',
    '/fraud/fraud-alerts',
    '/attendance/mark',
    '/attendance/mark-attendance',
    '/attendance/records',
]

headers = {'Authorization': f'Bearer {token}'}

print("\nEndpoint Status:")
print("-" * 50)
for endpoint in endpoints:
    url = f'http://localhost:8000{endpoint}'
    try:
        resp = requests.get(url, headers=headers, timeout=3)
        print(f"{endpoint:35} -> {resp.status_code}")
    except Exception as e:
        print(f"{endpoint:35} -> ERROR: {str(e)[:20]}")

print("\n✓ Test complete")

