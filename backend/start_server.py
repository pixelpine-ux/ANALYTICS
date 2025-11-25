#!/usr/bin/env python3
"""
Simple script to start the FastAPI server with uvicorn
"""
import sys
import os

# Add the virtual environment to Python path
venv_path = os.path.join(os.path.dirname(__file__), 'venv', 'lib', 'python3.12', 'site-packages')
sys.path.insert(0, venv_path)

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Retail Analytics API Server...")
    print("📊 Dashboard will be available at: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled for development")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )