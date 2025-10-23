#!/usr/bin/env python3
"""
Quick setup verification script for the Glow Beauty Salon AI System
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import sqlite3
        import asyncio
        import uvicorn
        import fastapi
        from fastapi.templating import Jinja2Templates
        from livekit.agents import Agent
        from livekit.plugins import groq, elevenlabs
        print("✅ All Python dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run 'uv sync' to install dependencies")
        return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        "src/agent.py",
        "src/database.py", 
        "src/web_server.py",
        "src/customer_followup.py",
        "src/timeout_service.py",
        "src/main.py",
        "templates/dashboard.html",
        ".env.example",
        "pyproject.toml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files are present")
        return True

def check_env_file():
    """Check if .env.local exists or provide guidance"""
    if os.path.exists(".env.local"):
        print("✅ .env.local file found")
        return True
    else:
        print("⚠️  .env.local not found - create it from .env.example")
        print("   cp .env.example .env.local")
        print("   Then add your API keys to .env.local")
        return True  # Not a blocker for initial setup

def test_database():
    """Test database initialization"""
    try:
        sys.path.insert(0, 'src')
        from database import Database
        
        db = Database()
        print("✅ Database initialization successful")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    print("🌟 Glow Beauty Salon AI System - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Files", check_files), 
        ("Environment", check_env_file),
        ("Database", test_database)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 Setup verification PASSED!")
        print("\n📋 Next Steps:")
        print("1. Ensure all API keys are in .env.local")
        print("2. Download models: uv run python src/agent.py download-files")
        print("3. Start system: uv run python src/main.py")
        print("4. Open dashboard: http://localhost:8000")
    else:
        print("❌ Setup verification FAILED - Fix issues above")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
