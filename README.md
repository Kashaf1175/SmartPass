# Smart Attendance Fraud Detection System

A full-stack attendance monitoring web application with fraud detection using a machine learning model.

## Tech Stack

- Frontend: React.js + Tailwind CSS
- Backend: Python + FastAPI
- Database: PostgreSQL (fallback to SQLite for local development)
- ML: Scikit-learn Isolation Forest

## Project Structure

- `backend/` - FastAPI backend, database models, ML model integration
- `frontend/` - React + Vite frontend with Tailwind styling

## Setup

### Backend

1. Open a terminal in `backend/`
2. Create a Python environment and install dependencies:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Set environment variables (optional):
   - `DATABASE_URL` for PostgreSQL connection string
   - `SECRET_KEY` for JWT signing
4. Start the backend:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend

1. Open a terminal in `frontend/`
2. Install dependencies:
   ```powershell
   npm install
   ```
3. Start the frontend:
   ```powershell
   npm run dev
   ```

## API Endpoints

- `POST /signup`
- `POST /login`
- `POST /mark-attendance`
- `GET /get-attendance`
- `GET /fraud-analysis`

## Notes

- The backend can run with SQLite locally using `sqlite:///./smartpass.db`.
- For production, configure `DATABASE_URL` for PostgreSQL.
- The application includes role-based access for student and admin users.
