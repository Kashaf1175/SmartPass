#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print('Current directory:', current_dir)
print('Python path:', sys.path)

try:
    from app.main import app
    print('✓ App imported successfully')
    import uvicorn
    print('✓ Uvicorn imported successfully')
    print('Starting server on http://0.0.0.0:8000...')
    uvicorn.run(app, host="0.0.0.0", port=8000)
except ImportError as e:
    print('✗ Import error:', e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print('✗ Other error:', e)
    import traceback
    traceback.print_exc()