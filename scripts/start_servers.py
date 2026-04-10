#!/usr/bin/env python3
"""
Script to start both backend and frontend servers.
"""

import sys
import subprocess
import time
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting FastAPI backend server...")
    backend_dir = Path(__file__).parent.parent / "server"
    try:
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Backend server started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"Failed to start backend server: {e}")
        return False

def start_frontend():
    """Start the React frontend server"""
    print("Starting React frontend server...")
    frontend_dir = Path(__file__).parent.parent / "client"
    try:
        subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Frontend server started on http://localhost:5173")
        return True
    except Exception as e:
        print(f"Failed to start frontend server: {e}")
        return False

def main():
    """Main function to start both servers"""
    print("Starting SmartPass servers...")

    # Start backend
    backend_started = start_backend()
    time.sleep(2)  # Wait a bit for backend to start

    # Start frontend
    frontend_started = start_frontend()

    if backend_started and frontend_started:
        print("\nBoth servers started successfully!")
        print("Backend API: http://localhost:8000")
        print("Frontend App: http://localhost:5173")
        print("API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop servers")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping servers...")
    else:
        print("Failed to start one or more servers")
        sys.exit(1)

if __name__ == "__main__":
    main()