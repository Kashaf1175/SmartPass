# SmartPass Authentication Setup - FIXED ✅

## Current Status

✅ **Backend (FastAPI)**
- Running on: `http://localhost:8000`
- Status: **ACTIVE** 
- Port: 8000
- MongoDB: Connected

✅ **Frontend (React/Vite)**
- Running on: `http://localhost:5176` (port 5175 was in use)
- Status: **ACTIVE**
- Note: Visit http://localhost:5176 NOT 5175

✅ **MongoDB**
- Running on: `mongodb://localhost:27017`
- Database: `smartpass`
- Status: **Connected**
- Collections: users, subjects, classes, attendances

## What Was Fixed

1. **Python Virtual Environment** - Reinstalled all dependencies properly
2. **Backend Startup** - Fixed module path and imports
3. **Database Connection** - Verified MongoDB connection working
4. **CORS Configuration** - Added support for all Vite dev ports (5173-5177)
5. **Frontend Port** - Added 5176/5177 to CORS allowed origins
6. **Error Handling** - Added network error detection and better error messages
7. **Email Normalization** - Emails are trimmed and lowercased
8. **Database Seeding** - Created test users and classes

## Test Credentials

### Admin Account
- **Email:** admin@smartpass.com
- **Password:** password123
- **Role:** admin

### Student Accounts
- **Email:** student1@smartpass.com through student5@smartpass.com
- **Password:** password123
- **Role:** student

## Available Classes

The database includes 6 classes across 5 subjects:
1. CS101 - Lecture A (Computer Science)
2. CS101 - Lab A (Computer Science)
3. MATH101 - Lecture B (Mathematics)
4. PHYS101 - Lecture C (Physics)
5. CHEM101 - Lab B (Chemistry)
6. BIO101 - Lecture D (Biology)

## How to Login

### Step 1: Open Browser
Go to: **http://localhost:5176** (NOT 5175)

### Step 2: Click "Create an account" or use existing credentials
- New Signup: Enter any email, set password
- Existing Login: Use credentials above

### Step 3: After Login
- **Admins:** Can create classes, manage subjects
- **Students:** Can mark attendance in available classes

## API Endpoints

All endpoints require Bearer token authentication:

### Authentication (No Auth Required)
- `POST /auth/signup` - Create new account
- `POST /auth/login` - Login and get token

### Classes & Subjects
- `GET /classes/subjects` - List all subjects
- `GET /classes/classes` - List all classes
- `POST /classes/subjects` - Create subject (Admin only)
- `POST /classes/classes` - Create class (Admin only)

### Attendance
- `POST /attendance/mark-attendance` - Mark attendance
- `GET /attendance/get-attendance` - Get attendance records

### Fraud Detection
- `GET /fraud/fraud-stats` - Get fraud analysis

## Network Error (if you see it)

If you see "Network Error: Cannot reach backend", it means:
1. Backend on port 8000 is not running
2. Check if error message shows actual backend URL

**Solution:** Restart backend with:
```bash
cd c:\Users\DELL\Desktop\SmartPass\server
c:/Users/DELL/Desktop/SmartPass/server/venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Quick Start (All Services Running)

1. **Backend** - Already running ✅
2. **Frontend** - Already running on http://localhost:5176 ✅
3. **Database** - Already seeded ✅

**Just open browser and go to:** http://localhost:5176

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot reach backend" | Backend crashed - check port 8000 |
| "Email already exists" | That email is taken, try another or use test account |
| "Invalid credentials" | Wrong password for that email |
| Port 5176 not loading | Try http://localhost:5177 or check npm output |
| Database empty | Run `python seed_data.py` again |

---
**Last Updated:** April 7, 2026
**Status:** All systems operational ✅
