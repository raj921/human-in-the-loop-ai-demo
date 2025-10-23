#!/usr/bin/env python3
"""
Test agent startup without LiveKit connection
"""

import sys
import asyncio
from unittest.mock import Mock, MagicMock

sys.path.insert(0, 'src')

from livekit.agents import JobContext, JobProcess, MetricsCollectedEvent
from livekit.plugins import groq, elevenlabs
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from agent import Assistant
from livekit.agents import AgentSession

# Mock the VAD
def create_mock_vad():
    mock_vad = Mock()
    return mock_vad

# Mock the JobProcess
def create_mock_job_process():
    mock_proc = Mock()
    mock_proc.userdata = {"vad": create_mock_vad()}
    return mock_proc

# Mock the JobContext
def create_mock_job_context():
    mock_ctx = Mock()
    mock_room = Mock()
    mock_room.name = "test_room"
    mock_ctx.room = mock_room
    mock_ctx.log_context_fields = {}
    mock_ctx.proc = create_mock_job_process()
    mock_ctx.add_shutdown_callback = Mock()
    mock_ctx.connect = Mock(return_value=asyncio.Future())
    mock_ctx.connect.return_value.set_result(None)
    return mock_ctx

async def test_agent_startup():
    print("🧪 Testing Agent Startup...")
    
    # Create mock context
    mock_ctx = create_mock_job_context()
    
    try:
        # Test that we can create the session configuration
        session = AgentSession(
            stt=groq.STT(model="whisper-large-v3-turbo"),
            llm=groq.LLM(model="llama-3.1-8b-instant"),
            tts=elevenlabs.TTS(voice_id="rachel"),
            turn_detection=MultilingualModel(),
            vad=mock_ctx.proc.userdata["vad"],
            preemptive_generation=True,
        )
        print("✅ AgentSession created successfully")
        
        # Test agent creation
        agent = Assistant()
        print("✅ Agent created successfully")
        
        print("🎉 Agent startup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Agent startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_agent_startup())
