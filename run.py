#!/usr/bin/env python3
"""
Quick start script - Chạy cả backend và mở frontend
"""

import subprocess
import webbrowser
import time
import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import yt_dlp
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\nPlease run: pip install -r requirements.txt")
        return False

def start_backend():
    """Start FastAPI backend"""
    print("\n🚀 Starting backend server...")
    backend_process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return backend_process

def start_frontend():
    """Start frontend HTTP server"""
    print("🌐 Starting frontend server...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return frontend_process

def main():
    print("=" * 50)
    print("🎥 Multi-Platform Video Downloader")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start backend
    backend = start_backend()
    time.sleep(2)  # Wait for backend to start
    
    # Start frontend
    frontend = start_frontend()
    time.sleep(1)  # Wait for frontend to start
    
    print("\n" + "=" * 50)
    print("✅ Servers are running!")
    print("=" * 50)
    print(f"📡 Backend API:  http://localhost:8000")
    print(f"🌐 Frontend:     http://localhost:3000")
    print("=" * 50)
    print("\n📝 Press Ctrl+C to stop servers\n")
    
    # Open browser
    time.sleep(1)
    webbrowser.open("http://localhost:3000")
    
    try:
        # Keep running
        backend.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        backend.terminate()
        frontend.terminate()
        print("✅ Servers stopped. Goodbye!")

if __name__ == "__main__":
    main()
