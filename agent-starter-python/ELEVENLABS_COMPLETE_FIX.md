# 🔊 ElevenLabs TTS - COMPLETE FIX GUIDE

## 🎯 **The Exact Problem:**
```
❌ Missing permission: "text_to_speech" 
❌ Missing permission: "voices_read"
❌ Voice "rachel" not found (probably due to missing permissions)
```

## 🔧 **COMPLETE SOLUTION (2 minutes)**

### **Step 1: Go to ElevenLabs**
👉 https://elevenlabs.io/app/settings/api-keys

### **Step 2: Create New API Key**
1. Click "**Create New API Key**"
2. **IMPORTANT** - Enable these permissions:
   - ✅ **Text to Speech** 
   - ✅ **Voices Read**
   - ✅ **User Details** (optional but recommended)
3. Give it a descriptive name: "**Glow Beauty Salon AI**"

### **Step 3: Copy the New Key**
Your new key will start with `sk_` and be longer than your current one.

### **Step 4: Update .env.local**
Replace your current ELEVEN_API_KEY:
```env
# Old key (remove this line)
ELEVEN_API_KEY=sk_your_old_short_key

# New key (add this line)
ELEVEN_API_KEY=sk_your_new_long_key_with_full_permissions
```

### **Step 5: Test the Fix**
```bash
# Test if permissions work
uv run python ELEVENLABS_TTS_FIX.py

# Run your agent
uv run python src/agent.py console
```

## 🎯 **What the Fix Will Accomplish:**

**Before (Current):**
```
❌ API Error: Missing text_to_speech permission
❌ API Error: Missing voices_read permission  
❌ TTS Error: Gateway connection closed
```

**After (Fixed):**
```
✅ Voices retrieved successfully
✅ Text-to-speech synthesis working
✅ Voice AI conversation complete
```

## 🎤 ** Common Working Voice IDs:**
Once you have permissions, these voices should work:
- `Domi` (most popular female voice)
- `Adam` (popular male voice)  
- `Bella`, `Elli`, `Josh`, `Sam`, `Rachel`

## 🚀 **Expected Result After Fix:**
```
🎤 You speak → ✅ Perfect speech recognition
🧠 AI processes → ✅ Intelligent response generated  
🔊 Voice output → ✅ Crystal clear audio plays
📊 Error-free logs → ✅ Complete system working
```

## 🎊 **Alternative: If You Need Help**

### **Check Your ElevenLabs Plan:**
- **Free Tier**: Limited voices and usage
- **Starter ($5/month)**: More voices and full permissions
- **Creator ($22/month)**: All features

### **If Still Issues:**
1. Make sure your ElevenLabs account is verified
2. Check your subscription status  
3. Try creating API key on a different browser
4. Contact ElevenLabs support if needed

## 📊 **Account Status Checker:**
```python
# Quick test to check your account
import asyncio
import aiohttp

async def check_account():
    api_key = "your_new_key_here"
    url = "https://api.elevenlabs.io/v1/user"
    headers = {"xi-api-key": api_key}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Account: {data.get('subscription', 'Unknown')}")
                print(f"✅ Character limit: {data.get('character_limit', 'Unknown')}")
                print(f"✅ Can use TTS: {data.get('can_use_tts', False)}")
            else:
                print(f"❌ Account check failed: {response.status}")

asyncio.run(check_account())
```

---

## 🎯 **Final Result:**

After following these steps, you'll have:
- ✅ Working ElevenLabs TTS with proper permissions
- ✅ Complete voice AI conversation with audio output
- ✅ Error-free agent operation
- ✅ Perfect human-in-the-loop AI receptionist

**Total time: 2 minutes to fix permissions and 1 minute to test!**

---

*Fix your ElevenLabs API key permissions and you'll have a 100% complete voice AI system!* 🎉
