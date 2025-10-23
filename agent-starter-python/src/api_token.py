"""
Token generation endpoint for LiveKit
"""
from fastapi import APIRouter, Query, HTTPException
from livekit import api
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

router = APIRouter()

@router.get("/api/token")
async def generate_token(room: str = Query(..., description="Room name")):
    """Generate LiveKit token for client connection"""
    try:
        # Get LiveKit credentials from environment
        api_key = os.getenv("LIVEKIT_API_KEY") or "APIrNeYY3MzFd6D"
        api_secret = os.getenv("LIVEKIT_API_SECRET") or "9KfRzEqLe3VkAGfbnEWfHneYJHoHGDs50AVO1HeJUd4M"
        
        if not api_key or not api_secret:
            raise HTTPException(status_code=500, detail="LiveKit credentials not configured")
        
        # Generate token
        token = api.AccessToken(api_key, api_secret) \
            .with_identity(f"user-{room}") \
            .with_name(f"Customer") \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room,
                can_publish=True,
                can_subscribe=True,
            ))
        
        return {"token": token.to_jwt()}
    
    except Exception as e:
        print(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail=str(e))
