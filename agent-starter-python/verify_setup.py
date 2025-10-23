#!/usr/bin/env python3
"""
Final verification script for the complete system
"""

import sys
import os

sys.path.insert(0, 'src')

print("🌟 GLOW BEAUTY SALON - FINAL SYSTEM VERIFICATION")
print("=" * 60)

# 1. Check environment variables
print("\n1️⃣ Checking environment configuration...")
required_vars = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET', 'GROQ_API_KEY', 'ELEVEN_API_KEY']
missing_vars = []

for var in required_vars:
    value = os.getenv(var)
    if value and value.startswith('your-'):
        print(f"⚠️  {var}: Placeholder value - needs real API key")
        missing_vars.append(var)
    elif not value:
        print(f"❌ {var}: Not set")
        missing_vars.append(var)
    else:
        print(f"✅ {var}: Configured")

# 2. Test imports
print("\n2️⃣ Testing component imports...")
try:
    from database import Database
    from agent import Assistant
    from web_server import app
    from customer_followup import CustomerFollowupService
    from timeout_service import TimeoutService
    from livekit.plugins import groq, elevenlabs
    print("✅ All components imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# 3. Test database
print("\n3️⃣ Testing database...")
try:
    db = Database()
    print("✅ Database initialized")
except Exception as e:
    print(f"❌ Database error: {e}")
    sys.exit(1)

# 4. Test agent configuration
print("\n4️⃣ Testing agent configuration...")
try:
    assistant = Assistant()
    print("✅ Agent created with salon context")
except Exception as e:
    print(f"❌ Agent error: {e}")
    sys.exit(1)

# 5. Test web server
print("\n5️⃣ Testing web server...")
try:
    from web_server import app
    print(f"✅ Web server created: {app.title}")
except Exception as e:
    print(f"❌ Web server error: {e}")
    sys.exit(1)

# 6. Check if templates exist
print("\n6️⃣ Checking templates...")
template_path = 'templates/dashboard.html'
if os.path.exists(template_path):
    print(f"✅ Dashboard template found: {template_path}")
else:
    print(f"❌ Dashboard template missing: {template_path}")
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 SYSTEM VERIFICATION COMPLETE")

if missing_vars:
    print(f"\n⚠️  ACTION REQUIRED:")
    print(f"   {len(missing_vars)} environment variables need real API keys:")
    for var in missing_vars:
        print(f"   - {var}")
    print(f"\n📋 To fix:")
    print(f"   1. Get API keys from service providers")
    print(f"   2. Update .env.local with real values")
    print(f"   3. Run: uv run python src/main.py")
else:
    print("\n✅ READY TO GO!")
    print("\n📋 Next steps:")
    print("   1. Run: uv run python src/main.py")
    print("   2. Open: http://localhost:8000")
    print("   3. Test the agent: uv run python src/agent.py console")

print("=" * 60)
