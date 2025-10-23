# 🔑 API Key Setup Guide

Follow these instructions to get all the required API keys for the Glow Beauty Salon AI System.

## 1. LiveKit Cloud 📡

1. **Sign Up**: Go to [LiveKit Cloud](https://cloud.livekit.io/)
2. **Create Application**: Click "New Application" and give it a name (e.g., "Glow Beauty Salon")
3. **Get Credentials**: In your application dashboard, you'll find:
   - **LiveKit URL**: `wss://your-app-id.livekit.cloud`
   - **API Key**: Starts with `DEV` or `PROD`
   - **API Secret**: Long secret key

**In `.env.local`:**
```env
LIVEKIT_URL=wss://your-app-id.livekit.cloud
LIVEKIT_API_KEY=DEVxxxxxxxxxxxxxxxxxx
LIVEKIT_API_SECRET=your-very-long-secret-key-here
```

> 💡 **Tip**: You can also use the LiveKit CLI to auto-populate these:
> ```bash
> lk cloud auth
> lk app env -w -d .env.local
> ```

## 2. Groq AI 🤖

1. **Sign Up**: Go to [Groq Console](https://console.groq.com/)
2. **Create API Key**: 
   - Go to "Keys" section
   - Click "Create Key"
   - Copy the key (starts with `gsk_`)

**In `.env.local`:**
```env
GROQ_API_KEY=gsk_your-groq-api-key-here
```

> 💡 **Free Tier**: Groq gives generous free limits perfect for testing

## 3. ElevenLabs 🎤

1. **Sign Up**: Go to [ElevenLabs](https://elevenlabs.io/)
2. **Get API Key**:
   - Go to your profile → Settings → API Keys
   - Click "Create API Key"
   - Copy the key

**In `.env.local`:**
```env
ELEVEN_API_KEY=your-elevenlabs-api-key-here
```

> 💡 **Free Tier**: ElevenLabs offers free credits for testing

## 4. Optional: Test Phone Number

For testing customer follow-up functionality, you can set a test phone number:

**In `.env.local`:**
```env
TEST_CUSTOMER_PHONE=+15551234567
```

> 💡 **Format**: Use E.164 format (country code + number, no spaces)

## 5. Verification

After adding all keys, verify your setup:

```bash
# Test the configuration
uv run python setup_test.py

# Download required models
uv run python src/agent.py download-files

# Start the system
uv run python src/main.py
```

## 🔒 Security Notes

- **Never commit** `.env.local` to version control
- **Keep keys secret** and don't share them
- **Use separate keys** for development and production
- **Rotate keys regularly** in production

## 🆘 Troubleshooting

### LiveKit Issues
- Ensure your app is "Active" in LiveKit Cloud
- Check if you're using the right URL (includes `/` at the end)
- Verify API key has correct permissions

### Groq Issues  
- Check if key starts with `gsk_`
- Verify you have available credits
- Try a different model if needed

### ElevenLabs Issues
- Verify key is not expired
- Check your usage limits
- Ensure you have selected a voice ID

### Common Error Messages

```
Error: Invalid API key
```
→ Double-check the key formatting and remove any extra spaces

```
Error: Out of credits
```
→ Check your service account limits or add payment methods

```
Error: Connection timeout
```
→ Verify your internet connection and firewall settings

## 📞 Need Help?

- **LiveKit Docs**: https://docs.livekit.io/
- **Groq Docs**: https://groq.com/docs/
- **ElevenLabs Docs**: https://elevenlabs.io/docs/
- **Project Issues**: Check the main README.md

---

Once you have all the API keys set up, run the system and open http://localhost:8000 to see the supervisor dashboard in action! 🎉
