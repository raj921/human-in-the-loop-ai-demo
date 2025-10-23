#!/usr/bin/env python3
"""
Get available ElevenLabs voices for TTS
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv('.env.local')

async def get_available_voices():
    print("🎤 ELEVENLABS AVAILABLE VOICES")
    print("=" * 40)
    
    api_key = os.getenv('ELEVEN_API_KEY')
    if not api_key:
        print("❌ ELEVEN_API_KEY not found")
        return None
    
    url = 'https://api.elevenlabs.io/v1/voices'
    headers = {
        'Accept': 'application/json',
        'xi-api-key': api_key
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    voices_data = await response.json()
                    
                    # Filter to English voices
                    english_voices = [
                        voice for voice in voices_data['voices'] 
                        if voice.get('language') == 'en'
                    ]
                    
                    print(f"✅ Found {len(english_voices)} English voices:")
                    print("\n🎤 Available Voices (choose one for agent.py):")
                    
                    for i, voice in enumerate(english_voices[:10]):  # Show first 10
                        voice_id = voice.get('voice_id', 'Unknown')
                        name = voice.get('name', 'Unknown')
                        gender = voice.get('gender', 'Unknown')
                        age_range = voice.get('age', 'Unknown')
                        print(f"   {i+1:2d}. {voice_id:20} - {name:20} ({gender}/{age_range})")
                    
                    if len(english_voices) > 10:
                        print(f"   ... and {len(english_voices)-10} more voices")
                    
                    # Find the most common/popular voices
                    print("\n🌟 RECOMMENDED VOICES:")
                    popular_voices = [
                        'Adam', 'Bella', 'Domi', 'Elli', 'Josh', 'Rachel', 'Sam'
                    ]
                    
                    for voice_id in popular_voices:
                        voice_exists = any(v.get('voice_id').lower() == voice_id.lower() 
                                       for v in english_voices)
                        if voice_exists:
                            print(f"   ✅ {voice_id}")
                        else:
                            print(f"   ❌ {voice_id} (not available)")
                    
                    # Find the first available voice
                    if english_voices:
                        first_voice = english_voices[0].get('voice_id')
                        print(f"\n💡 QUICK FIX: Use this voice ID: '{first_voice}'")
                        return first_voice
                    
                else:
                    error_text = await response.text()
                    print(f"❌ Error getting voices: {error_text}")
                    return None
                    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

async def update_agent_with_voice(voice_id):
    print(f"\n🔧 UPDATING AGENT.PY WITH VOICE: {voice_id}")
    
    try:
        with open('src/agent.py', 'r') as f:
            content = f.read()
        
        # Find and replace the voice line
        import re
        
        # Look for the line with elevenlabs.TTS
        pattern = r'tts=elevenlabs\.TTS\(voice_id="[^"]+"\)'
        replacement = f'tts=elevenlabs.TTS(voice_id="{voice_id}")'
        
        if re.search(pattern, content):
            updated_content = re.sub(pattern, replacement, content)
            
            with open('src/agent.py', 'w') as f:
                f.write(updated_content)
            
            print(f"✅ Updated agent.py to use voice: {voice_id}")
            return True
        else:
            print("❌ Could not find TTS line to update in agent.py")
            return False
            
    except Exception as e:
        print(f"❌ Error updating agent.py: {e}")
        return False

async def main():
    voice_id = await get_available_voices()
    
    if voice_id:
        update_success = await update_agent_with_voice(voice_id)
        
        if update_success:
            print(f"\n🎉 FIX COMPLETE!")
            print(f"   ✅ Updated agent.py with working voice: {voice_id}")
            print(f"   🧪 Test now: uv run python src/agent.py console")
        else:
            print(f"\n⚠️ Manual update required:")
            print(f"   Edit src/agent.py line ~163:")
            print(f"   Change: tts=elevenlabs.TTS(voice_id=\"rachel\")")  
            print(f"   To:     tts=elevenlabs.TTS(voice_id=\"{voice_id}\")")
    else:
        print("\n❌ Could not fix automatically")
        print("   Check your ElevenLabs account and subscription")

if __name__ == "__main__":
    asyncio.run(main())
