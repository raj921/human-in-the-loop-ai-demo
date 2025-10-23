#!/usr/bin/env python3
"""
ElevenLabs TTS Permission Fix Guide
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv('.env.local')

async def show_elevenlabs_status():
    print("🔍 ELEVENLABS TTS STATUS CHECK")
    print("=" * 45)
    
    api_key = os.getenv('ELEVEN_API_KEY')
    
    if not api_key:
        print("❌ ELEVEN_API_KEY not found in .env.local")
        return False
    
    if api_key.startswith('your-'):
        print("❌ You're still using placeholder key")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Test the API
    url = 'https://api.elevenlabs.io/v1/text-to-speech/rachel'
    headers = {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': api_key
    }
    data = {
        'text': 'Hello, this is a test.',
        'model_id': 'eleven_monolingual_v1'
    }
    
    try:
        print("🌐 Testing ElevenLabs TTS API...")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    print(f"✅ SUCCESS: ElevenLabs TTS working!")
                    print(f"   Received {len(audio_data)} bytes of audio")
                    return True
                elif response.status == 401:
                    error_text = await response.text()
                    print("❌ PERMISSION ERROR (401):")
                    print("   Your API key is missing text-to-speech permission")
                    print("   Error details:", error_text)
                    return False
                else:
                    error_text = await response.text()
                    print(f"❌ API ERROR ({response.status}):")
                    print("   Error details:", error_text)
                    return False
                    
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        return False

async def main():
    working = await show_elevenlabs_status()
    
    print("\n" + "=" * 45)
    
    if working:
        print("🎉 ElevenLabs TTS is already working!")
        print("   Your agent should work fine now.")
    else:
        print("🔧 QUICK FIX STEPS:")
        print("   1. Go to: https://elevenlabs.io/app/settings/api-keys")
        print("   2. Click 'Create New API Key'")
        print("   3. ✅ Enable 'Text to Speech' permission")
        print("   4. Give it a name like 'Glow Beauty Salon AI'")
        print("   5. Copy the new key")
        print("   6. Update .env.local:")
        print("      ELEVEN_API_KEY=sk_your_new_key")
        print("\n   ⏰ Total time: 2 minutes")
        print("   🧪 Then test: uv run python src/agent.py console")

if __name__ == "__main__":
    asyncio.run(main())
